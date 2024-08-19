from pygame import Vector2
import pygame
from engine.ecs import Entity, EntityGroup
from engine.window import Window
from systems.tilemap import TilemapComponent, parse_tile_map


def init(group: EntityGroup, _: Window):
    map = parse_tile_map('maps/game-map.png')

    tilemap = Entity("tilemap")
    tilemap.tilemap = TilemapComponent.from_map(map)
    group.add(tilemap)

    pygame.font.init()