from engine.ecs import Entity, EntityGroup, enumerate_component
from pygame import Vector2
from .motion import MotionComponent
from .turn import TurnComponent
from .player import PlayerComponent

from .enemy import create_enemy

import random
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

    # Create 4 enemies at random locations for testing.
    for i in range(2):
        position = (random.choice(range(-10,10)),random.choice(range(-10,10)))
        group.add(create_enemy(position))

    group.mount_system(testing_system)
