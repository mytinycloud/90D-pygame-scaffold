from engine.entity import Entity, EntityGroup
from engine.window import Window

from .sprites import with_placeholder_sprite
from .position import with_position


'''
The player update system
'''
def player_update_system(group: EntityGroup):

    player = group.query_singleton('is_player')
    # Do any player specific handling.


'''
Adds the player character
'''
def mount_player_system(group: EntityGroup):
    player = group.create()
    player.is_player = True
    with_position(player, (0,0))
    with_placeholder_sprite(player, (32,32), (255,0,0))

    group.mount_system(player_update_system)