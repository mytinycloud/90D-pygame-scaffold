from engine.ecs import Entity, EntityGroup, enumerate_component, factory
from pygame import Vector2
from dataclasses import dataclass
import random
import math

from .sprites import SpriteComponent
from .motion import MotionComponent
from .controls import ControlComponent
from .tilemap import TilemapComponent
from . import turn
from . import tilemap
from . import utils


SHAPE_NONE = 0
SHAPE_WAVE = 1
SHAPE_FILL = 2
SHAPE_LANCE = 3


'''
Component class to store effect information
'''
@enumerate_component("effect")
class EffectComponent():
    direction: Vector2 = factory(Vector2)
    energy: int = 1
    shape: int = SHAPE_NONE
    harvests: dict[int,tuple[int,int]] = factory(dict)
    chains_to: dict[int,tuple[float,int]] = factory(dict)
    cast_from: list[int]

    def add_harvest(self, tile_in: int, tile_out: int, energy: int):
        self.harvests[tile_in] = (tile_out, energy)

    def add_chain(self, tile_in: int, probability: float = 1.0, energy: int = 0):
        self.chains_to[tile_in] = (probability, energy)

'''
Return the normal vectors for a given direction
'''
def vector_normals(pos: Vector2, diretion: Vector2) -> list[Vector2]:
    return (
        pos + utils.rotate_vector_cw(diretion),
        pos + utils.rotate_vector_ccw(diretion)
    )

'''
Return the 4 cardinal directions
'''
def vector_cardinals(pos: Vector2) -> list[Vector2]:
    return (
        pos + Vector2(1,0),
        pos + Vector2(0,1),
        pos + Vector2(-1,0),
        pos + Vector2(0,-1)
    )

'''
Enumerates through the valid targets for a given effect
'''
def valid_tiles(map: TilemapComponent, valid: list[int], coords: list[Vector2]):
    return [ coord for coord in coords if (map.get_tile(coord) in valid) ]

'''
Shuffles the list.
Note this mutates the given list. I dont care.
'''
def shuffled(items: list) -> list:
    random.shuffle(items)
    return items

'''
The effect update system:
Handles effect propigation and decay (probably)
'''
def effect_update_system(group: EntityGroup):

    t: turn.TurnComponent = group.query_singleton("turn").turn

    if t.state != turn.TURN_EFFECTS:
        return
    
    map: TilemapComponent = group.query_singleton('tilemap').tilemap

    for e in group.query("effect", "motion"):
        
        effect: EffectComponent = e.effect
        motion: MotionComponent = e.motion
        pos = motion.position
        dir = effect.direction

        # Harvesting
        tile = map.get_tile(pos)
        if tile in effect.harvests:
            new_tile, energy_gain = effect.harvests[tile]
            map.set_tile(pos, new_tile)
            effect.energy += energy_gain
        
        # Propagation
        if effect.energy > 1:

            # A list of places we would like to try propagate to.
            # (position, energy, shape)
            propagation_request: list[tuple[Vector2, int, int]] = []
            unchecked_coords = []

            # Do the forced propagation, which is shape specific
            if effect.shape == SHAPE_WAVE:
                # Waves transfer all energy forward.
                propagation_request = [
                    (pos + dir, effect.energy - 1, SHAPE_WAVE),
                ]

                # Waves start waves in valid adjacent tiles
                for coord in valid_tiles(map, effect.cast_from, vector_normals(pos, dir)):
                    propagation_request.append( (coord, 0, SHAPE_WAVE) )
                unchecked_coords = [-dir]

            elif effect.shape == SHAPE_FILL:
                # Goes out in all directions
                valid_coords = valid_tiles(map, effect.cast_from, shuffled(vector_cardinals(pos)))
                # Let the propagation step figure out if we use more energy than we have...
                energy_transfer =  math.ceil(effect.energy) / energy_transfer
                for coord in valid_coords:
                    propagation_request.append( (coord, energy_transfer, SHAPE_FILL) )

            elif effect.shape == SHAPE_LANCE:
                # Goes forward only
                propagation_request = [
                    (pos + dir, effect.energy - 1, SHAPE_LANCE),
                ]
                unchecked_coords = list(vector_normals(pos, dir)) + [-dir]

            else: # SHAPE_NONE
                unchecked_coords = vector_cardinals(pos)

            # Do the random propagation in the unchecked directions
            for coord in shuffled( valid_tiles(map, effect.chains_to, unchecked_coords) ):
                probability, energy = effect.chains_to[map.get_tile(coord)]
                if random.random() < probability:
                    propagation_request.append( (coord, energy, SHAPE_NONE) )
            
            # Apply the propagation requests
            for coord, energy, shape in propagation_request:
                energy = min(energy, max(0, effect.energy -1))              
                group.add( propagate_entity(e, coord, energy, shape) )
      

        # decay
        effect.energy -= 1
        if effect.energy <= 0:
            group.remove(e)


'''
Propagates an existing effect, inheriting some energy. Shape may be overridden here.
'''
def propagate_entity(e: Entity, position: Vector2, energy: int, shape: int | None = None) -> Entity:
    # Remove the energy from the previous effect
    e.effect.energy -= energy

    # Create the new effect
    e = e.clone()
    e.motion.position = position
    e.effect.energy = energy

    # The shape may be overridden
    if shape != None:
        e.effect.shape = shape

    return e


'''
Instantiate all the template effects. These can be cloned when required
'''
def create_effect_templates():
    effect_dict = {}

    e = Entity("effect-fire")
    e.motion = MotionComponent()
    e.sprite = SpriteComponent.from_circle(16, (255,0,0))
    e.effect = EffectComponent(cast_from=[tilemap.TILE_EMBER])
    e.effect.add_harvest(tilemap.TILE_PLANT, tilemap.TILE_EMBER, 3)
    e.effect.add_harvest(tilemap.TILE_WATER, tilemap.TILE_MUD, -3)
    e.effect.add_harvest(tilemap.TILE_MUD, tilemap.TILE_EARTH, -1)
    e.effect.add_chain(tilemap.TILE_PLANT, 0.5)
    effect_dict["fire"] = e

    e = Entity("effect-wave")
    e.motion = MotionComponent()
    e.sprite = SpriteComponent.from_circle(16, (0,0,255))
    e.effect = EffectComponent(cast_from=[tilemap.TILE_WATER],shape=SHAPE_WAVE)
    e.effect.add_harvest(tilemap.TILE_WATER, tilemap.TILE_MUD, 3)
    e.effect.add_harvest(tilemap.TILE_EARTH, tilemap.TILE_MUD, 0)
    effect_dict["wave"] = e

    e = Entity("effect-growth")
    e.motion = MotionComponent()
    e.sprite = SpriteComponent.from_circle(16, (0,255,0))
    e.effect = EffectComponent(cast_from=[tilemap.TILE_MUD])
    e.effect.add_harvest(tilemap.TILE_MUD, tilemap.TILE_PLANT, 10)
    e.effect.add_harvest(tilemap.TILE_EARTH, tilemap.TILE_PLANT, 0)
    e.effect.add_chain(tilemap.TILE_MUD, 0.25)
    e.effect.add_chain(tilemap.TILE_EARTH, 0.25)
    effect_dict["growth"] = e

    e = Entity("effect-spark")
    e.motion = MotionComponent()
    e.sprite = SpriteComponent.from_circle(16, (255,255,0))
    e.effect = EffectComponent(cast_from=[tilemap.TILE_EMBER], shape=SHAPE_LANCE)
    e.effect.add_harvest(tilemap.TILE_EMBER, tilemap.TILE_EARTH, 2)
    effect_dict["spark"] = e
    
    return effect_dict

EFFECT_TEMPLATES = create_effect_templates()


'''
Spawns a new effect (as per a spell)
'''
def create_effect(type: str, position: Vector2, direction: Vector2 = Vector2(0)) -> Entity:
    e = EFFECT_TEMPLATES[type].clone()
    e.motion.position = Vector2(position)
    e.effect.direction = direction
    return e


'''
Mounts the effect updating system
'''
def mount_effect_system(group: EntityGroup):
    group.mount_system(effect_update_system)
