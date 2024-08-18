from engine.ecs import Entity, EntityGroup, enumerate_component
import os

import pygame
from pygame.surface import Surface
from pygame import Color, Vector2

from systems.tilemap import TILE_SPRITES, TilemapComponent

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
    tilemap: TilemapComponent = group.query_singleton('tilemap').tilemap
    surface: Surface = camera.camera.surface
    scale = camera.camera.scale
    origin = Vector2(surface.get_size()) / 2 - (camera.motion.position * scale)
    sprite_scale = Vector2(scale)

    for y, row in enumerate(tilemap.map):
        for x, tile in enumerate(row):
            if not tilemap.contains((x, y)):
                continue

            tile_surface = TILE_SPRITES[tile]
            scaled_tile = pygame.transform.scale(tile_surface, sprite_scale)
            size = Vector2(scaled_tile.get_size())
            position = Vector2(x, y) * scale + origin - size / 2
            surface.blit(scaled_tile, position)

    for e in sorted((e for e in group.query('sprite', 'motion') if (e.motion.layer != None)), key = lambda e: -e.motion.layer):
        
        motion: MotionComponent = e.motion
        sprite: SpriteComponent = e.sprite

        scaled_sprite = pygame.transform.scale(sprite.surface, sprite_scale)

        size = Vector2(scaled_sprite.get_size())
        sprite_pos = motion.position * scale + origin - size / 2

        # Note, we are ignoring any screen-space culling
        surface.blit(scaled_sprite, sprite_pos)

def camera_update_system(group: EntityGroup):
    camera_entity = group.query_singleton('camera', 'motion')
    camera_motion: MotionComponent = camera_entity.motion
    camera: CameraComponent = camera_entity.camera
    tilemap: TilemapComponent = group.query_singleton('tilemap').tilemap
    camera_motion.position = tilemap.bounds.topleft + (Vector2(tilemap.bounds.width) - Vector2(1)) / 2
    scale_size = min(camera.surface.get_width(), camera.surface.get_height())
    camera.scale = scale_size / tilemap.bounds.width

    

'''
Mounts the sprite drawing system, and adds a camera component for the viewport
'''
def mount_sprite_system(group: EntityGroup, target: Surface):
    camera = Entity("camera")
    camera.camera = CameraComponent(surface=target)
    camera.motion = MotionComponent(position=Vector2(0,0))
    group.add(camera)

    group.mount_system(camera_update_system)
    group.mount_system(draw_sprite_system)

