from engine.ecs import Component, Entity, EntityGroup, enumerate_component
from engine.window import Window

from .motion import MotionComponent

import pygame
import os


'''
A component that contains sprite information
'''
@enumerate_component("sprite")
class SpriteComponent(Component):
    def __init__(self, surface: pygame.surface.Surface):
        self.surface = surface

    '''
    Creates a sprite from a resource file
    '''
    @staticmethod
    def from_resource(resource: str) -> 'SpriteComponent':
        resource = os.path.join("resources", resource)
        surface = pygame.image.load(resource)
        return SpriteComponent(surface)
    
    '''
    Creates a filled square as a sprite
    '''
    @staticmethod
    def from_square(size: tuple[int,int], color: tuple[int,int,int]):
        surface = pygame.surface.Surface(size)
        surface.fill(color)
        return SpriteComponent(surface)


'''
A component that represents a camera
'''
@enumerate_component("camera")
class CameraComponent():
    def __init__(self, window: Window):
        self.window = window


'''
The sprite drawings system:
Use the camera position to draw all entities with a sprite at their relative location.
'''
def draw_sprite_system(group: EntityGroup):

    camera = group.query_singleton('camera')
    window: Window = camera.camera.window
    origin = (
        (window.res[0] / 2) - camera.motion.position[0],
        (window.res[1] / 2) - camera.motion.position[1]
    )

    for e in group.query('sprite', 'motion'):
        
        size = e.sprite.surface.get_size()
        sprite_pos = (
            e.motion.position[0] + origin[0] - (size[0] / 2),
            e.motion.position[1] + origin[1] - (size[1] / 2)
        )
        # Note, we are ignoring any screen-space culling
        window.surface.blit(e.sprite.surface, sprite_pos)


'''
Mounts the sprite drawing system, and adds a camera component for the viewport
'''
def mount_sprite_system(group: EntityGroup, window: Window):
    camera = Entity("camera")
    camera.camera = CameraComponent(window)
    camera.motion = MotionComponent((0,0))
    group.add(camera)
    
    group.mount_system(draw_sprite_system)

