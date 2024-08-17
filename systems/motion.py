from engine.ecs import EntityGroup, enumerate_component, factory
from pygame import Vector2

'''
Component containing a position, velocity, ect
'''
@enumerate_component("motion")
class MotionComponent():
    position: Vector2 = factory(Vector2)
    velocity: Vector2 = factory(Vector2)

'''
The motion update system:
Update any entities with motions components
'''
def motion_update_system(group: EntityGroup):

    # Update the position of all entities with a velocity
    for e in group.query('motion'):
        motion: MotionComponent = e.motion
        motion.position += motion.velocity

'''
Mounts systems for updating motion components
'''
def mount_motion_system(group: EntityGroup):
    group.mount_system(motion_update_system)

