from engine.entity import Entity, EntityGroup
from engine.window import Window


'''
Adds position information to an entity
'''
def with_position(e: Entity, position: tuple[float,float]):
    e.pos = position

