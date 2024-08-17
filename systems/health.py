from engine.ecs import EntityGroup, enumerate_component

@enumerate_component("health")
class HealthComponent:
    health: int

'''
Update health system for 
'''
def update_health_system(group: EntityGroup):
    pass


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
    print('new player health: ', player.health.health)
    return
