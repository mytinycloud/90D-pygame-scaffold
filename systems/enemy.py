from pygame import Vector2
from engine.ecs import Entity, EntityGroup, enumerate_component
from .motion import MotionComponent
from .sprites import SpriteComponent
from .player import PlayerComponent
from .turn import TurnComponent

from math import copysign
from random import choice

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

    player: PlayerComponent = group.query_singleton('player')
    turn: TurnComponent = group.query_singleton('turn').turn

    if (turn.state != 2):
        return 
    
    for e in group.query('enemy'):

        motion: MotionComponent = e.motion
        mtp = move_towards_player(player.motion.position, e.motion.position)
        motion.velocity = mtp


def mount_enemy_system(group: EntityGroup):
    group.mount_system(enemy_update_system)

def move_towards_player(p_pos: Vector2, e_pos: Vector2):

    """ 
        Current implementation allows running in a diagonal
        Want the system to choose the larger of either x or y values 
        and set the other to zero 

        if Δ_x is !== 0, then do difference calculation
        if Δ_y is !== 0, then do difference calculation
        choose which one to randomly use
    """  

    new_x = p_pos.x - e_pos.x
    new_y = p_pos.y - e_pos.y
    
    velocity_x = Vector2(copysign(1.0, new_x), 0)
    velocity_y = Vector2(0, copysign(1.0, new_y))

    # Both equally far away, choose random one
    if (new_x != 0 and new_y != 0):
        print('not in plane', new_x, new_y)
        print('choice:', choice([velocity_x, velocity_y]))
        return choice([velocity_x, velocity_y])

    if (new_x != 0):
        print('returning x')
        return velocity_x
    else:
        print('returning y')
        return velocity_y
    
def create_enemy(position = tuple[int, int]):
    enemy = Entity("enemy")
    # enemy.health = #Hc
    # enemy.motion = #motion
    enemy.enemy = EnemyComponent()
    enemy.sprite = SpriteComponent.from_circle(diameter=30, color=(0,123,123))
    enemy.motion = MotionComponent(position=Vector2(position[0],position[1]))

    return enemy