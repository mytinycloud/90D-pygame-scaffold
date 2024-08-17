from engine.ecs import Entity, EntityGroup, enumerate_component, factory
from pygame import Vector2
from dataclasses import dataclass
import random

from .sprites import SpriteComponent
from .motion import MotionComponent
from .controls import ControlComponent
from .tilemap import TilemapComponent
from . import turn
from . import tilemap
from . import utils


SHAPE_WAVE = 0
SHAPE_FILL = 1


'''
Component class to store effect information
'''
@enumerate_component("effect")
class EffectComponent():
    direction: Vector2 = factory(Vector2)
    energy: int = 1
    shape: int = SHAPE_WAVE
    harvests: dict[int,tuple[int,int]] = factory(dict)
    propagates: dict[int,tuple[int, float]] = factory(dict)

    def add_harvest(self, tile_in: int, tile_out: int, energy: int):
        self.harvests[tile_in] = (tile_out, energy)

    def add_propagation(self, tile_in: int, energy_tranfer: int = 0, probability: float = 1.0):
        self.propagates[tile_in] = (energy_tranfer, probability)

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

            propagation_coords = []

            if effect.shape == SHAPE_WAVE:
                # Waves transfer all energy forward.
                energy_transfer = effect.energy - 1
                group.add(propagate_entity(e, pos + dir, energy_transfer))
                effect.energy -= energy_transfer
                propagation_coords = vector_normals(pos, dir)

            if effect.shape == SHAPE_FILL:
                # Goes out in all directions
                propagation_coords = vector_cardinals(pos)

            for coord in propagation_coords:
                tile = map.get_tile(coord)
                if tile in effect.propagates:
                    energy_transfer,probability = effect.propagates[tile]
                    if random.random() < probability:
                        energy_transfer = max(0, min(energy_transfer, effect.energy - 1))
                        effect.energy -= energy_transfer
                        group.add(propagate_entity(e, coord, energy_transfer))

        # decay
        effect.energy -= 1
        if effect.energy <= 0:
            group.remove(e)


'''
Propagates an existing effect, inheriting some energy
'''
def propagate_entity(e: Entity, position: Vector2, energy: int) -> Entity:
    e = e.clone()
    e.motion.position = position
    e.effect.energy = energy
    return e


'''
Instantiate all the template effects. These can be cloned when required
'''
def create_effect_templates():
    effect_dict = {}

    e = Entity("effect-fire")
    e.motion = MotionComponent()
    e.sprite = SpriteComponent.from_circle(16, (255,0,0))
    e.effect = EffectComponent(shape=SHAPE_FILL)
    e.effect.add_harvest(tilemap.TILE_PLANT, tilemap.TILE_EMBER, 3)
    e.effect.add_harvest(tilemap.TILE_WATER, tilemap.TILE_MUD, -3)
    e.effect.add_harvest(tilemap.TILE_MUD, tilemap.TILE_EARTH, -1)
    e.effect.add_propagation(tilemap.TILE_PLANT)
    effect_dict["fire"] = e

    e = Entity("effect-wave")
    e.motion = MotionComponent()
    e.sprite = SpriteComponent.from_circle(16, (0,0,255))
    e.effect = EffectComponent(shape=SHAPE_WAVE)
    e.effect.add_harvest(tilemap.TILE_WATER, tilemap.TILE_MUD, 3)
    e.effect.add_harvest(tilemap.TILE_EARTH, tilemap.TILE_MUD, 0)
    e.effect.add_propagation(tilemap.TILE_WATER)
    effect_dict["wave"] = e

    e = Entity("effect-growth")
    e.motion = MotionComponent()
    e.sprite = SpriteComponent.from_circle(16, (0,255,0))
    e.effect = EffectComponent(shape=SHAPE_FILL)
    e.effect.add_harvest(tilemap.TILE_MUD, tilemap.TILE_PLANT, 10)
    e.effect.add_harvest(tilemap.TILE_EARTH, tilemap.TILE_PLANT, 0)
    e.effect.add_propagation(tilemap.TILE_MUD, 5, 0.25)
    e.effect.add_propagation(tilemap.TILE_EARTH, 5, 0.25)
    effect_dict["growth"] = e
    

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
