from engine.ecs import EntityGroup
from pygame import Vector2

from systems.controls import ControlComponent
from systems.sprites import CameraComponent

from .motion import MotionComponent

'''
Will have the camera follow the player if it is locked, otherwise controls will move the camera
'''
def camera_control_system(group: EntityGroup):
    camera_entity: MotionComponent = group.query_singleton('camera')
    camera: CameraComponent = camera_entity.camera
    camera_motion: MotionComponent = camera_entity.motion
    controls: ControlComponent = group.query_singleton('controls').controls

    if "camera_lock_start" in controls.actions:
        camera.is_locked = not camera.is_locked

    if camera.is_locked:
        player_motion = group.query_singleton('player').motion
        camera_motion.position = Vector2(player_motion.position)
    else:
        camera_motion.velocity = controls.direction * 250

    


'''
Mounts the camera control system
'''
def mount_camera_control_system(group: EntityGroup):
    group.mount_system(camera_control_system)

