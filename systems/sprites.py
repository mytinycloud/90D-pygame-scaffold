from engine.entity import Entity, EntityGroup
from engine.window import Window

from .position import with_position

import pygame
import os

'''
The sprite drawings system.

Use the camera position to draw all entities with a sprite at their relative location.
'''
def draw_sprite_system(group: EntityGroup):

    camera = group.query_singleton('camera_target')
    window: Window = camera.camera_target

    for e in group.query('sprite', 'pos'):
        
        local_x = e.pos[0] - camera.pos[0]
        local_y = e.pos[1] - camera.pos[1]

        # Todo. Actually be good.
        screen_x = local_x
        screen_y = local_y

        window.surface.blit(e.sprite, (screen_x, screen_y))


'''
Adds the sprite drawing system, along with its rendering camera
'''
def mount_sprite_system(group: EntityGroup, window: Window):
    camera = group.create()
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

