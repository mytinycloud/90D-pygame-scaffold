from engine.ecs import Entity, EntityGroup, enumerate_component

from .sprites import SpriteComponent
from .motion import MotionComponent


'''
Component class to store player specific information
'''
@enumerate_component("player")
class PlayerComponent():
    pass


'''
The player update system:
Update the players velocity based on the controls
'''
def player_update_system(group: EntityGroup):

    camera = group.query_singleton('camera').camera
    if not camera.is_locked:
        return

    controls = group.query_singleton('controls').controls


'''
Adds the player character, and mounts systems for updating the player with the control inputs
'''
def mount_player_system(group: EntityGroup):
    player = Entity("player")
    player.player = PlayerComponent()
    player.motion = MotionComponent()
    player.sprite = SpriteComponent.from_box((32, 32), (255,0,0))
    group.add(player)

    group.mount_system(player_update_system)
