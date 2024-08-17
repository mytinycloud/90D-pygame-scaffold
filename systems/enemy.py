from pygame import Vector2
from engine.ecs import Entity, EntityGroup, enumerate_component
from .motion import MotionComponent
from .sprites import SpriteComponent
from .player import PlayerComponent
from .turn import TurnComponent
from .health import HealthComponent
from . import turn

from math import copysign
from random import choice

'''
A component that represents a generic enemy
'''
@enumerate_component("enemy")
class EnemyComponent:
    damage: int

'''
Update enemy systems only taking into account when it's the enemies turn
'''
def enemy_update_system(group: EntityGroup):

    player: PlayerComponent = group.query_singleton('player')
    t: TurnComponent = group.query_singleton('turn').turn

    if (t.state != turn.TURN_ENEMY):
        return 
    
    for e in group.query('enemy'):

        motion: MotionComponent = e.motion
        mtp = move_towards_player(player.motion.position, e.motion.position)
        motion.velocity = mtp

'''
Mount system
'''
def mount_enemy_system(group: EntityGroup):
    group.mount_system(enemy_update_system)

'''
Naive pathing implementation to move towards player one 
step at a time. If the enemy is not in either x or y plane, then choose
a random plane to move on. 
'''
def move_towards_player(p_pos: Vector2, e_pos: Vector2):

    delta = p_pos - e_pos
    print(delta)
    
    velocity_x = Vector2(copysign(1.0, delta.x), 0)
    velocity_y = Vector2(0, copysign(1.0, delta.y))

    # If neither are in plane with player, choose random one
    if (delta.x != 0 and delta.y != 0):
        return choice([velocity_x, velocity_y])

    if (delta.x != 0):
        return velocity_x
    else:
        return velocity_y

def create_enemy(position = tuple[int, int]):
    enemy = Entity("enemy")
    enemy.enemy = EnemyComponent(damage = 10)
    enemy.sprite = SpriteComponent.from_circle(diameter = 30, color = (0,123,123))
    enemy.motion = MotionComponent(position = Vector2(position[0],position[1]))
    enemy.health = HealthComponent(health = 100)

    return enemy