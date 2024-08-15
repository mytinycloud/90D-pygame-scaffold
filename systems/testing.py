from engine.ecs import Entity, EntityGroup, enumerate_component
from pygame import Vector2

from .sprites import SpriteComponent
from .motion import MotionComponent
from .collisions import HitboxComponent

'''
Just a place to add some in-development / testing code
'''
def testing_system(group: EntityGroup):

    player = group.query_singleton("player")
    motion = player.motion
    controls = group.query_singleton("controls").controls

    if "spawn_start" in controls.actions:
        e = Entity("box")
        e.motion = MotionComponent(position=Vector2(controls.mouse_camera_position))
        e.sprite = SpriteComponent.from_box((32,32), (0,0,255))
        e.hitbox = HitboxComponent.from_box((32,32), 1)
        group.add(e)

    if len(player.hitbox.intersections):
        for intersection in player.hitbox.intersections:
            player.motion.position -= intersection.overlap


'''
Mount the testing system any testing init
'''
def mount_testing_system(group: EntityGroup):

    e = Entity("box")
    e.motion = MotionComponent(position=Vector2(100,100))
    e.sprite = SpriteComponent.from_box((32,32), (0,0,255))
    e.hitbox = HitboxComponent.from_box((32,32), 1)
    group.add(e)

    e = e.clone()
    e.motion.position = Vector2(150,90)
    e.hitbox = HitboxComponent.from_circle(32, 1)
    e.sprite = SpriteComponent.from_circle(32, (0,0,255))
    group.add(e)

    group.mount_system(testing_system)
