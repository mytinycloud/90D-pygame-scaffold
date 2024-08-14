from engine.ecs import EntityGroup, enumerate_component, factory
from pygame import Vector2

'''
Component containing a position, velocity, ect
'''
@enumerate_component("motion")
class MotionComponent():
    position: Vector2 = factory(Vector2)
    velocity: Vector2 = factory(Vector2)
    is_movable: bool = False

'''
The motion update system:
Update any entities with motions components
'''
def motion_update_system(group: EntityGroup):

    # Naughty. Get this from the window?
    delta = group.query_singleton("time").time.delta
    
    # Update the position of all entities with a velocity
    for e in group.query('motion'):
        motion: MotionComponent = e.motion
        if motion.is_movable:
            motion.position += motion.velocity * delta

'''
Mounts systems for updating motion components
'''
def mount_motion_system(group: EntityGroup):
    group.mount_system(motion_update_system)

