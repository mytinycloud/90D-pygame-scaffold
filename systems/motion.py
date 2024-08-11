from engine.entity import Entity, EntityGroup
from engine.window import Window


'''
The motion update system:
Update any entities with motions components
'''
def motion_update_system(group: EntityGroup):

    # Naughty. Get this from the window?
    timestep = 1.0 / 60
    
    # Update the position of all entities with a velocity
    for e in group.query('velocity'):
        e.pos = (
            e.pos[0] + (e.velocity[0] * timestep),
            e.pos[1] + (e.velocity[1] * timestep),
        )

'''
Mounts systems for updating motion components
'''
def mount_motion_system(group: EntityGroup):
    group.mount_system(motion_update_system)

'''
Adds position information to an entity
'''
def with_position(e: Entity, position: tuple[float,float]):
    e.pos = position

'''
Adds motion information to an entity.
with_position is implied.
'''
def with_motion(e: Entity, position: tuple[float, float]):
    e.pos = position
    e.velocity = (0,0)

