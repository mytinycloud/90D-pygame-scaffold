from typing import TypeVar
from pygame import Color, image
from engine.ecs import enumerate_component, factory

TILE_EARTH = 0
TILE_WATER = 1
TILE_MUD = 2
TILE_PLANT = 3
TILE_EMBER = 4

EA = TILE_EARTH
WA = TILE_WATER
MU = TILE_MUD
PL = TILE_PLANT
EM = TILE_EMBER

Tilemap = list[list[int]]

def rgb_key(rgba: tuple[int, int, int, int]):
    key = ''
    for part in rgba:
        key += '_' + str(part)

    return key

TILE_COLOR_MAP = {
    rgb_key(Color('#67584b')): TILE_EARTH,
    rgb_key(Color('#4772e5')): TILE_WATER,
    rgb_key(Color('#5d330e')): TILE_MUD,
    rgb_key(Color('#6ad127')): TILE_PLANT,
    rgb_key(Color('#e04a09')): TILE_EMBER
}

'''
Component that stores a tilemap
'''
@enumerate_component("tilemap")
class TilemapComponent():
    map: list[list[int]] = factory([
        [EA,EA,EA,EA,EA,EA,EA,EA,EA,EA],
        [EA,WA,WA,WA,EA,EA,EA,EA,EA,EA],
        [EA,EA,EA,EA,EA,EA,EA,EA,EA,EA],
        [EA,EA,EA,EA,EA,EA,EA,EA,EA,EA],
        [EA,EA,EA,MU,MU,MU,EA,EA,EA,EA],
        [EA,EA,EA,MU,MU,EA,EA,EA,EA,EA],
        [EA,EA,EA,EA,EA,EA,EM,EM,EA,EA],
        [EA,PL,PL,EA,EA,EA,EM,EA,EA,EA],
        [EA,EA,EA,EA,EA,EA,EA,EA,EA,EA],
        [EA,EA,EA,EA,EA,EA,EA,EA,EA,EA],
    ])

def parse_tile_map(image_path: str) -> Tilemap:
    map_surface = image.load(image_path)
    map: Tilemap = list()
    for y in range(map_surface.get_height()):
        map.append(list())
        for x in range(map_surface.get_width()):
            tile = TILE_COLOR_MAP[rgb_key(map_surface.get_at((x, y)))] or TILE_EARTH
            map[y].append(tile)
    
    return map
