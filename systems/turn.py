from engine.ecs import Entity, EntityGroup, enumerate_component, factory
from enum import Enum


TURN_PLAYER = 0
TURN_EFFECTS = 1
TURN_ENEMY = 2
TURN_COMPLETE = 3


'''
Component class to store time information
'''
@enumerate_component("turn")
class TurnComponent():
    number: int = 0
    state: int = TURN_PLAYER
    waiting: bool = True # waiting for user input



'''
Moves the game time information into the time entity
'''
def update_turn_system(group: EntityGroup):
    
    turn: TurnComponent = group.query_singleton("turn").turn

    if not turn.waiting:
        turn.state += 1
        if turn.state == TURN_COMPLETE:
            turn.state = TURN_PLAYER
            turn.waiting = True
            turn.number += 1
    


'''
Mounts the components and systems for reading controls
'''
def mount_turn_system(group: EntityGroup):
    e = Entity("turn")
    e.turn = TurnComponent()
    group.add(e)
    group.mount_system(update_turn_system)
