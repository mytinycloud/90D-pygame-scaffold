from engine.ecs import Entity, EntityGroup
from engine.window import Window
from systems.tilemap import TilemapComponent


def init(group: EntityGroup, window: Window):
    tilemap = Entity("tilemap")
    tilemap.tilemap = TilemapComponent()
    
    group.add(tilemap)