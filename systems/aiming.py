from engine.ecs import EntityGroup
from pygame import Vector2

from systems.controls import ControlComponent

from .motion import MotionComponent

'''
Will have the player entity "aim" at the mouse position when the right mouse button is held down
'''
def aiming_system(group: EntityGroup):
    player_motion: MotionComponent = group.query_singleton('player', 'motion').motion
    controls: ControlComponent = group.query_singleton('controls').controls

    if 'mouse_2' in controls.actions:
        player_motion.rotation = (controls.mouse_camera_position - player_motion.position).angle_to(Vector2(1,0))
    else:
        player_motion.rotation = 0


'''
Mounts the aiming system
'''
def mount_aiming_system(group: EntityGroup):
    group.mount_system(aiming_system)

