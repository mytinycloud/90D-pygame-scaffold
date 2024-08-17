from engine.ecs import Entity, EntityGroup, enumerate_component
from pygame import Vector2
from .motion import MotionComponent
from .turn import TurnComponent
from .player import PlayerComponent

from .enemy import create_enemy
from .effect import create_effect

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
    enemy1 = create_enemy((-5,5))
    group.add(enemy1)
    group.mount_system(testing_system)
