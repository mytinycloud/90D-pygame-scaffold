from engine.ecs import Entity, EntityGroup, enumerate_component
from .motion import MotionComponent

@enumerate_component("enemy")
class EnemyComponent:
    # Inherit health
    # Inherit position
    # Implement 
        # attacks
        # clone 
            # Position
            # Health 
    pass

def enemy_update_system(group: EntityGroup):

    for e in group.query('enemy'):
        motion: MotionComponent = e.motion
        # Update position
        # Position
        # Check if in contact with player
            # If true 
                # Deal damage to player
                # Reduce health to zero
    print('updating enemy')


def mount_enemy_system(group: EntityGroup):
    group.mount_system(enemy_update_system)