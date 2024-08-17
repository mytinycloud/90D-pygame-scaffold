from engine.ecs import EntityGroup, enumerate_component
from .turn import TurnComponent

from . import turn

@enumerate_component("health")
class HealthComponent:
    health: int

'''
Update health system for 
'''
def update_health_system(group: EntityGroup):

    p = group.query_singleton('player')
    t:TurnComponent = group.query_singleton('turn').turn

    if (t.state == turn.TURN_ENEMY or t.state == turn.TURN_PLAYER):
        for e in group.query('enemy', 'health'):
            if p.motion.position == e.motion.position:
                reduce_player_health(p, e.enemy.damage)
                group.remove(entity = e)

'''
Mount health system
'''
def mount_health_system(group: EntityGroup):
    group.mount_system(update_health_system)
    pass

'''
Reduce the player health by the value specified, typically drawn
directly from the enemy component damage value
'''
def reduce_player_health(player, value):
    player.health.health -= value 
    print('new player health: ', player.health)
    return
