from engine.ecs import Entity, EntityGroup, enumerate_component
from pygame import Vector2
from .motion import MotionComponent
from .turn import TurnComponent
from .player import PlayerComponent

from .enemy import create_enemy

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
    enemy1 = create_enemy((-10,20))
    # enemy2 = create_enemy((40,-60))
    # enemy3 = create_enemy((-50,-70))
    # enemy4 = create_enemy((70,70))
    group.add(enemy1)
    # group.add(enemy2)
    # group.add(enemy3)
    # group.add(enemy4)
    group.mount_system(testing_system)
