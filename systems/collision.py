from engine.ecs import Entity, EntityGroup, enumerate_component, factory
import typing

from pygame import Vector2

from .motion import MotionComponent
from . import motion


'''
A component that does collision detection
'''
@enumerate_component("collision")
class CollisionComponent():
    lookup = {}
    layers: list[list[Entity]] = factory(list)

    def get_entities_at(self, pos: Vector2, layer: int) -> typing.Generator[Entity,None,None]:
        for e in self.layers[layer]:
            if e.motion.position == pos:
                yield e

    def is_occupied(self, pos: Vector2, layer: int) -> bool:
        for e in self.layers[layer]:
            if e.motion.position == pos:
                return True
        return False
        
    @staticmethod
    def from_layer_count(layers: int) -> 'CollisionComponent':
        return CollisionComponent(layers=[ [] for _ in range(layers) ])



'''
The sprite drawings system:
Use the camera position to draw all entities with a sprite at their relative location.
'''
def collision_system(group: EntityGroup):

    collisions: CollisionComponent = group.query_singleton("collision").collision

    for layer in collisions.layers:
        layer.clear()

    for e in group.query("motion"):
        motion: MotionComponent = e.motion
        if motion.layer != None:
            collisions.layers[motion.layer].append(e)


'''
Mounts the sprite drawing system, and adds a camera component for the viewport
'''
def mount_collision_system(group: EntityGroup):
    e = Entity("collision")
    e.collision = CollisionComponent.from_layer_count(motion.LAYER_COUNT)
    group.add(e)

    group.mount_system(collision_system)

