
'''
A component that represents a camera
'''
from engine.ecs import enumerate_component

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


@enumerate_component("tilemap")
class TilemapComponent():
    map = [
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
    ]

