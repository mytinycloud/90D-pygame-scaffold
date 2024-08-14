from engine.ecs import Entity, EntityGroup, enumerate_component
import os

import pygame
from pygame.surface import Surface
from pygame import Vector2

from .motion import MotionComponent



'''
A component that contains sprite information
'''
@enumerate_component("sprite")
class SpriteComponent():
    surface: Surface

    '''
    Creates a sprite from a resource file
    '''
    @staticmethod
    def from_resource(resource: str) -> 'SpriteComponent':
        resource = os.path.join("resources", resource)
        surface = pygame.image.load(resource)
        return SpriteComponent(surface=surface)
    
    '''
    Creates a filled square as a sprite
    '''
    @staticmethod
    def from_box(size: tuple[int,int], color: tuple[int,int,int]):
        surface = Surface(size)
        surface.fill(color)
        return SpriteComponent(surface=surface)
    
    '''
    Creates a filled circle as a sprite
    '''
    @staticmethod
    def from_circle(diameter: int, color: tuple[int,int,int]):
        surface = Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(surface, color, Vector2(diameter/2), diameter/2)
        return SpriteComponent(surface=surface)


'''
A component that represents a camera
'''
@enumerate_component("camera")
class CameraComponent():
    surface: Surface


'''
The sprite drawings system:
Use the camera position to draw all entities with a sprite at their relative location.
'''
def draw_sprite_system(group: EntityGroup):

    camera = group.query_singleton('camera')
    surface = camera.camera.surface
    origin = Vector2(surface.get_size()) / 2 - camera.motion.position

    for e in group.query('sprite', 'motion'):
        
        size = Vector2(e.sprite.surface.get_size())
        sprite_pos = e.motion.position + origin - size / 2

        # Note, we are ignoring any screen-space culling
        surface.blit(e.sprite.surface, sprite_pos)


'''
Mounts the sprite drawing system, and adds a camera component for the viewport
'''
def mount_sprite_system(group: EntityGroup, target: Surface):
    camera = Entity("camera")
    camera.camera = CameraComponent(surface=target)
    camera.motion = MotionComponent()
    group.add(camera)
    
    group.mount_system(draw_sprite_system)

