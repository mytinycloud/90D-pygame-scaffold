from engine.ecs import Entity, EntityGroup, enumerate_component
from pygame import Vector2


'''
Just a place to add some in-development / testing code
'''
def testing_system(group: EntityGroup):
    pass


'''
Mount the testing system any testing init
'''
def mount_testing_system(group: EntityGroup):
    group.mount_system(testing_system)
