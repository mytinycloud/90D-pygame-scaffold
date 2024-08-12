from engine.entity import Entity, EntityGroup
from engine.window import Window

from .sprites import with_placeholder_sprite
from .motion import with_position, with_motion


'''
The player update system:
Update the players velocity based on the controls
'''
def player_update_system(group: EntityGroup):

    player = group.query_singleton('is_player')
    controls = group.query_singleton('controls').controls

    player.velocity = (
        controls.direction[0] * 100,
        controls.direction[1] * 100,
    )


'''
Adds the player character, and mounts systems for updating the player with the control inputs
'''
def mount_player_system(group: EntityGroup):
    player = group.create("player")
    player.is_player = True
    with_motion(player, (0,0))
    with_placeholder_sprite(player, (32,32), (255,0,0))

    group.mount_system(player_update_system)