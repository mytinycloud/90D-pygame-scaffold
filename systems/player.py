from engine.ecs import Entity, EntityGroup, enumerate_component
from pygame import Vector2

from .sprites import SpriteComponent
from .motion import MotionComponent
from .controls import ControlComponent
from .health import HealthComponent
from . import turn
from . import motion


'''
Component class to store player specific information
'''
@enumerate_component("player")
class PlayerComponent():
    pass

def get_direction_command(actions: list[str]) -> Vector2 | None:
    mapping = {
        "up_start": Vector2(0,-1),
        "down_start": Vector2(0,1),
        "left_start": Vector2(-1,0),
        "right_start": Vector2(1,0),
    }
    for key in mapping:
        if key in actions:
            return mapping[key]
    return None

'''
The player update system:
Update the players velocity based on the controls
'''
def player_update_system(group: EntityGroup):

    t: turn.TurnComponent = group.query_singleton("turn").turn
    player = group.query_singleton('player', 'motion', 'health')

    if t.state != turn.TURN_PLAYER or not player.health.is_alive:
        # Nothing we can do
        return

    controls: ControlComponent = group.query_singleton('controls').controls

    dir_command = get_direction_command(controls.actions)
    if dir_command:
        player.motion.velocity = dir_command
        t.waiting = False

    if "skip_start" in controls.actions:
        t.waiting = False



'''
Adds the player character, and mounts systems for updating the player with the control inputs
'''
def mount_player_system(group: EntityGroup):
    player = Entity("player")
    player.player = PlayerComponent()
    player.motion = MotionComponent(layer=motion.LAYER_PLAYER, position=Vector2(128,128))
    player.sprite = SpriteComponent.from_box((32, 32), (255,0,0))
    player.health = HealthComponent(health = 100)
    group.add(player)

    group.mount_system(player_update_system)
