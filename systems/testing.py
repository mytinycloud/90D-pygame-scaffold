from engine.ecs import Entity, EntityGroup, enumerate_component
from pygame import Vector2

from .sprites import SpriteComponent
from .motion import MotionComponent
from .collisions import HitboxComponent

'''
Just a place to add some in-development / testing code
'''
def testing_system(group: EntityGroup):
    pass


'''
Mount the testing system and any testing code
'''
def mount_testing_system(group: EntityGroup):
    
    e = Entity("box")
    e.motion = MotionComponent(Vector2(100,100))
    e.sprite = SpriteComponent.from_box((32,32), (0,0,255))
    e.hitbox = HitboxComponent.from_box((32,32))
    group.add(e)

    e = e.clone()
    e.motion.position = Vector2(150,90)
    group.add(e)

    group.mount_system(testing_system)