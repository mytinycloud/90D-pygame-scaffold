from engine.ecs import Entity, EntityGroup, enumerate_component, factory
from pygame import Vector2

from .sprites import SpriteComponent
from .motion import MotionComponent
from .controls import ControlComponent
from . import turn


EFFECT_WAVE = 0
EFFECT_FILL = 1


'''
Component class to store effect information
'''
@enumerate_component("effect")
class EffectComponent():
    direction: Vector2 = factory(Vector2)
    energy: int = 1
    type: bool = EFFECT_WAVE



'''
The effect update system:
Handles effect propigation and decay (probably)
'''
def effect_update_system(group: EntityGroup):

    t: turn.TurnComponent = group.query_singleton("turn").turn

    if t.state != turn.TURN_EFFECTS:
        return

    for e in group.query("effect", "motion"):
        
        effect: EffectComponent = e.effect
        motion: MotionComponent = e.motion
        
        # Propagation
        if effect.energy > 1:
            if effect.type == EFFECT_WAVE:
                # all energy is transferred to the new entity
                energy_transfer = effect.energy - 1
                group.add(propagate_entity(e, motion.position + effect.direction, energy_transfer))
                effect.energy -= energy_transfer

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
    e.effect = EffectComponent()
    e.effect.energy = 3
    effect_dict["fire"] = e

    e = Entity("effect-wave")
    e.motion = MotionComponent()
    e.sprite = SpriteComponent.from_circle(16, (0,0,255))
    e.effect = EffectComponent()
    e.effect.energy = 3
    effect_dict["wave"] = e

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

    group.add( create_effect("wave", Vector2(3,3), Vector2(1,0) ) )
