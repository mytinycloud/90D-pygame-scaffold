from engine.ecs import Entity, EntityGroup, enumerate_component, factory

from pygame.time import Clock


'''
Component class to store time information
'''
@enumerate_component("time")
class TimeComponent():
    clock: Clock
    total: float = 0.0      # Game time in seconds
    delta: float = 0.0      # Elapsed time since previous frame
    tick: int = 0           # Frame number



'''
Moves the game time information into the time entity
'''
def update_time_system(group: EntityGroup):
    
    t: TimeComponent = group.query_singleton("time").time

    delta = t.clock.get_time() / 1000.0
    t.tick += 1
    t.delta = delta
    t.total += delta



'''
Mounts the component and systems for providing game time
'''
def mount_time_system(group: EntityGroup, clock: Clock):
    e = Entity("time")
    e.time = TimeComponent(clock = clock)
    group.add(e)
    group.mount_system(update_time_system)
