from engine.entity import Entity, EntityGroup
from engine.window import Window

from .motion import with_position

import pygame
import os

'''
The sprite drawings system:
Use the camera position to draw all entities with a sprite at their relative location.
'''
def draw_sprite_system(group: EntityGroup):

    camera = group.query_singleton('camera_target')
    window: Window = camera.camera_target
    origin = (
        (window.res[0] / 2) - camera.pos[0],
        (window.res[1] / 2) - camera.pos[1]
    )

    for e in group.query('sprite', 'pos'):
        
        size = e.sprite.get_size()
        sprite_pos = (
            e.pos[0] + origin[0] - (size[0] / 2),
            e.pos[1] + origin[1] - (size[1] / 2)
        )
        # Note, we are ignoring any screen-space culling
        window.surface.blit(e.sprite, sprite_pos)


'''
Mounts the sprite drawing system, and adds a camera component for the viewport
'''
def mount_sprite_system(group: EntityGroup, window: Window):
    camera = group.create("camera")
    camera.camera_target = window
    with_position(camera, (0,0))
    
    group.mount_system(draw_sprite_system)

'''
Adds sprite information to an entity
'''
def with_sprite(e: Entity, resource: str):
    resource = os.path.join("resources", resource)
    e.sprite = pygame.image.load(resource)
    

'''
Adds a wretched placeholder box as a sprite
'''
def with_placeholder_sprite(e: Entity, size: tuple[int,int], color: tuple[int,int,int]):
    surface = pygame.surface.Surface(size)
    surface.fill(color)
    e.sprite = surface

