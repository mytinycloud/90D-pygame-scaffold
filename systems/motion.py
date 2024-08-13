from engine.ecs import Component, EntityGroup, enumerate_component
from pygame import Vector2

'''
Component containing a position, velocity, ect
'''
@enumerate_component("motion")
class MotionComponent(Component):
    def __init__(self, pos: Vector2 = Vector2(0,0), is_movable: bool = False):
        self.position = Vector2(pos)
        self.velocity = Vector2(0,0)
        self.is_movable = is_movable

'''
The motion update system:
Update any entities with motions components
'''
def motion_update_system(group: EntityGroup):

    # Naughty. Get this from the window?
    timestep = 1.0 / 60
    
    # Update the position of all entities with a velocity
    for e in group.query('motion'):
        motion: MotionComponent = e.motion
        if motion.is_movable:
            motion.position += motion.velocity * timestep

'''
Mounts systems for updating motion components
'''
def mount_motion_system(group: EntityGroup):
    group.mount_system(motion_update_system)

