from engine.entity import Entity, EntityGroup
from engine.window import Window

def draw_sprites(group: EntityGroup):

    camera = group.query('camera_target')
    window: Window = camera.camera_target

    for e in group.query('sprite'):
        
        local_x = e.pos[0] - camera.pos[0]
        local_y = e.pos[1] - camera.pos[1]

        # TODO: Screenspace culling


'''
Adds camera information to an entity
'''
def with_camera(e: Entity, window: Window):
    e.camera_target = window

'''
Adds sprite information to an entity
'''
def with_sprite(e: Entity, sprite: str):
    e.sprite = pygame

