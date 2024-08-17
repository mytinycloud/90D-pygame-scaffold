from engine.ecs import Entity, EntityGroup, enumerate_component, factory
from pygame import Vector2

from .sprites import SpriteComponent
from .motion import MotionComponent
from .controls import ControlComponent
from . import turn


'''
Component class to store effect information
'''
@enumerate_component("effect")
class EffectComponent():
    direction: Vector2 = factory(Vector2)
    energy: int = 0
    is_wave: bool = True



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
            if effect.is_wave:
                # all energy is transferred to the new entity
                energy_transfer = effect.energy - 1
                group.add(propagate_entity(e, motion.position + effect.direction, energy_transfer))
                effect.energy -= energy_transfer

        # decay
        effect.energy -= 1
        if effect.energy <= 0:
            group.remove(e)
        


def propagate_entity(e: Entity, position: Vector2, energy: int) -> Entity:
    e = e.clone()
    e.motion = MotionComponent(position=position)
    e.effect.energy = energy
    return e

def create_effect(position: Vector2, energy: int = 3) -> Entity:
    e = Entity("effect")
    e.motion = MotionComponent(position=Vector2(position))
    e.sprite = SpriteComponent.from_circle(16, (255,0,0))
    e.effect = EffectComponent(direction=Vector2(1,0),energy=energy)
    return e


'''
Mounts the effect updating system
'''
def mount_effect_system(group: EntityGroup):
    group.mount_system(effect_update_system)

    group.add( create_effect(Vector2(3,3)) )
