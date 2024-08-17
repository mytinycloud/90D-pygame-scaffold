import dataclasses
from pygame import Surface, Vector2
from engine.ecs import Entity, EntityGroup, enumerate_component
from systems import tilemap
from systems.controls import ControlComponent
from systems.effect import EffectComponent, create_effect
from systems.motion import MotionComponent
from systems.turn import TurnComponent
from systems.ui import UIComponent
from systems.utils import clamp_vector

@enumerate_component("spell")
class SpellComponent:
    select_action: str
    effect: str = "wave"


@enumerate_component("selected_spell")
class SelectedSpellComponent:
    spell_action: str = None
    spell_casting_start: Vector2 = None

def spell_select_system(group: EntityGroup):
    actions = group.query_singleton('controls').controls.actions
    selected_spell_entity = group.query_singleton('selected_spell')
    selected_spell: SelectedSpellComponent = selected_spell_entity.selected_spell
    ui: UIComponent = selected_spell_entity.ui

    for spell_entity in group.query('spell'):
        spell: SpellComponent = spell_entity.spell

        if spell.select_action in actions or selected_spell.spell_action is None:
            selected_spell.spell_action = spell.select_action
            ui.text = spell_entity.name
            break


def spell_cast_system(group: EntityGroup):
    controls: ControlComponent = group.query_singleton('controls').controls
    selected_spell_entity: SelectedSpellComponent = group.query_singleton('selected_spell')
    selected_spell: SelectedSpellComponent = selected_spell_entity.selected_spell
    turn: TurnComponent = group.query_singleton('turn').turn

    if not turn.waiting:
        return

    if "mouse_0_start" in controls.actions:
        selected_spell.spell_casting_start = controls.mouse_grid_position
    if "mouse_0_stop" in controls.actions:
        for spell_entity in group.query('spell'):
            spell: SpellComponent = spell_entity.spell
            if spell.select_action == selected_spell.spell_action:
                effect_direction = clamp_vector(controls.mouse_grid_position - selected_spell.spell_casting_start, Vector2(-1,-1), Vector2(1,1))
                effect_entity = create_effect(spell.effect, selected_spell.spell_casting_start, effect_direction)
                group.add(effect_entity)
                turn.waiting = False
                break
        selected_spell.spell_casting_start = None

def mount_spell_system(group: EntityGroup):
    water_wave = Entity("Water wave")
    water_wave.spell = SpellComponent(select_action="select_spell_1", effect="wave")
    plant_growth = Entity("Plant growth")
    plant_growth.spell = SpellComponent(select_action="select_spell_2", effect="growth")
    spark = Entity("Spark")
    spark.spell = SpellComponent(select_action="select_spell_3", effect="spark")

    selected_spell_entity = Entity("selected_spell")
    selected_spell_entity.selected_spell = SelectedSpellComponent()
    selected_spell_entity.ui = UIComponent(text="")
    selected_spell_entity.motion = MotionComponent(position=Vector2(50, 50))

    group.add_all(water_wave, plant_growth, spark)
    group.add(selected_spell_entity)

    group.mount_system(spell_select_system)
    group.mount_system(spell_cast_system)