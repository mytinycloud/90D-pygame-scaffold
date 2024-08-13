from engine.ecs import Component, Entity, EntityGroup, enumerate_component
from engine.window import Window

import pygame


'''
Component class to store decoded control inputs
'''
@enumerate_component("controls")
class ControlComponent(Component):
    def __init__(self):
        self.direction: tuple[int,int] = (0,0)


'''
The controls handling system:
Read inputs from the keyboard, and store them in the controls component
'''
def update_controls_system(group: EntityGroup):
    controls: ControlComponent = group.query_singleton('controls').controls
    keys = pygame.key.get_pressed()
    
    controls.direction = (
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
