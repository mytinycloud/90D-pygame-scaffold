from engine.ecs import Entity, EntityGroup, enumerate_component


'''
Component class to store lifetime information
'''
@enumerate_component("lifetime")
class LifetimeComponent():
    duration: float
    started: float = -1


'''
System to remove entities that have expired
'''
def lifetime_system(group: EntityGroup):

    now: float = group.query_singleton("time").time.total
    
    for e in group.query("lifetime"):
        lifetime: LifetimeComponent = e.lifetime
        if lifetime.started < 0:
            lifetime.started = now
        if now - lifetime.started >= lifetime.duration:
            group.remove(e)


'''
Mount the lifetime system
'''
def mount_lifetime_system(group: EntityGroup):
    group.mount_system(lifetime_system)