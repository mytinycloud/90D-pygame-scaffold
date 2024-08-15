from engine.ecs import Entity, EntityGroup, enumerate_component, factory

import pygame
from pygame import Vector2

key_mapping = {
    pygame.K_w: ["up"],
    pygame.K_a: ["left"],
    pygame.K_s: ["down"],
    pygame.K_d: ["right"],
    pygame.K_LSHIFT: ["sprint"],
    pygame.K_SPACE: ["spawn"],
}

'''
Component class to store decoded control inputs
'''
@enumerate_component("controls")
class ControlComponent():
    direction: Vector2 = factory(Vector2)
    actions: list =  factory(list)
    mouse_position: Vector2 = factory(Vector2)
    mouse_camera_position: Vector2 = factory(Vector2)

'''
The controls handling system:
Read inputs from the keyboard, and store them in the controls component
'''
def update_controls_system(group: EntityGroup):

    controls: ControlComponent = group.query_singleton('controls').controls
    past_actions = controls.actions
    controls.actions = list()
    keys = pygame.key.get_pressed()

    for key in key_mapping:
        for action in key_mapping[key]:
            if keys[key]:
                controls.actions.append(action)
                if past_actions.count(action) == 0:
                    controls.actions.append(action + "_start")
            elif past_actions.count(action) > 0:
                controls.actions.append(action + "_end")

    mouse = pygame.mouse.get_pos()
    controls.mouse_position = Vector2(mouse)
    camera = group.query_singleton('camera', 'motion')
    motion = camera.motion
    surface = camera.camera.surface
    controls.mouse_camera_position = mouse + motion.position - Vector2(surface.get_size()) / 2

    controls.direction = Vector2(
        int(keys[pygame.K_d]) - int(keys[pygame.K_a]),
        int(keys[pygame.K_s]) - int(keys[pygame.K_w])
    )


'''
Mounts the components and systems for reading controls
'''
def mount_control_system(group: EntityGroup):
    controls = Entity("controls")
    controls.controls = ControlComponent()
    group.add(controls)

    group.mount_system(update_controls_system)
