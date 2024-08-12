from engine.entity import Entity, EntityGroup
from engine.window import Window

import pygame


'''
Dataclass to contain decoded input information
'''
class ControlComponent():
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
def mount_control_system(group: EntityGroup, window: Window):
    controls = group.create("controls")
    controls.controls = ControlComponent()
    
    group.mount_system(update_controls_system)
