from engine.ecs import Entity, EntityGroup
from engine.window import Window
from systems.tilemap import TilemapComponent, parse_tile_map


def init(group: EntityGroup, window: Window):
    map = parse_tile_map('assets/map.png')

    tilemap = Entity("tilemap")
    tilemap.tilemap = TilemapComponent(map = map)
    
    group.add(tilemap)