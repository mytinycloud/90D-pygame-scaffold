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
    z: float = 0

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


TILE_SCALE = 32

'''
A component that represents a camera
'''
@enumerate_component("camera")
class CameraComponent():
    surface: Surface
    scale: float = TILE_SCALE


'''
The sprite drawings system:
Use the camera position to draw all entities with a sprite at their relative location.
'''
def draw_sprite_system(group: EntityGroup):

    camera = group.query_singleton('camera', 'motion')
    surface: Surface = camera.camera.surface
    origin = Vector2(surface.get_size()) / 2 - camera.motion.position

    scale = camera.camera.scale

    sprite_scale = Vector2(camera.camera.scale / TILE_SCALE)

    for e in sorted(group.query('sprite', 'motion'), key = lambda e: e.sprite.z):
        
        motion: MotionComponent = e.motion
        sprite: SpriteComponent = e.sprite
        
        size = Vector2(sprite.surface.get_size())
        sprite_pos = motion.position * scale + origin - size / 2

        scaled_sprite = pygame.transform.scale_by(sprite.surface, sprite_scale)

        # Note, we are ignoring any screen-space culling
        surface.blit(scaled_sprite, sprite_pos)


'''
Mounts the sprite drawing system, and adds a camera component for the viewport
'''
def mount_sprite_system(group: EntityGroup, target: Surface):
    camera = Entity("camera")
    camera.camera = CameraComponent(surface=target)
    camera.motion = MotionComponent()
    group.add(camera)

    group.mount_system(draw_sprite_system)

