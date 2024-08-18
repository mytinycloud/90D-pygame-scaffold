from engine.ecs import EntityGroup, enumerate_component

@enumerate_component("health")
class HealthComponent:
    health: int
    is_alive: bool = True

'''
Update health system for 
'''
def update_health_system(group: EntityGroup):
    for e in group.query("health"):
        if e.health.health <= 0:
            e.health.is_alive = False


'''
Mount health system
'''
def mount_health_system(group: EntityGroup):
    group.mount_system(update_health_system)
    pass

