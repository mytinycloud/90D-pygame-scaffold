from engine.ecs import Component, Entity, EntityGroup, enumerate_component

from .sprites import SpriteComponent
from .motion import MotionComponent


'''
Component class to store player specific information
'''
@enumerate_component("player")
class PlayerComponent(Component):
    def __init__(self):
        pass


'''
The player update system:
Update the players velocity based on the controls
'''
def player_update_system(group: EntityGroup):

    controls = group.query_singleton('controls').controls

    for player in group.query('player'):
        player.motion.velocity = controls.direction * 100


'''
Adds the player character, and mounts systems for updating the player with the control inputs
'''
def mount_player_system(group: EntityGroup):
    player = Entity("player")
    player.player = PlayerComponent()
    player.motion = MotionComponent(is_movable = True)
    player.sprite = SpriteComponent.from_square((32,32), (255,0,0))
    group.add(player)

    group.mount_system(player_update_system)