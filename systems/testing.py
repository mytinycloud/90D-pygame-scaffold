from engine.ecs import Entity, EntityGroup, enumerate_component
from pygame import Vector2
from .motion import MotionComponent
from .turn import TurnComponent
from .player import PlayerComponent

from .enemy import create_enemy
from .effect import create_effect

from random import choice
'''
Just a place to add some in-development / testing code
'''
def testing_system(group: EntityGroup):
    # player: PlayerComponent = group.query_singleton('player')
    # print(player.motion.position)
    pass

'''
Mount the testing system any testing init
'''
def mount_testing_system(group: EntityGroup):
    group.add(create_enemy((8,5)))

    # Create group of enemies randomly placed on map.
    for i in range(4):
        enemy = create_enemy((choice(range(5,15)), choice(range(5,15))))
        group.add(enemy)

    #group.add(create_effect("wave", Vector2(2,3), Vector2(1,0)))
    #group.add(create_effect("fire", Vector2(3,10)))
    #group.add(create_effect("growth", Vector2(9,5)))
    group.mount_system(testing_system)
