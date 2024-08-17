import dataclasses
from pygame import Vector2
from engine.ecs import Entity, EntityGroup, enumerate_component
from systems import tilemap
from systems.controls import ControlComponent
from systems.effect import EffectComponent, create_effect
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
    selected_spell: SelectedSpellComponent = group.query_singleton('selected_spell').selected_spell

    for spell_entity in group.query('spell'):
        spell: SpellComponent = spell_entity.spell

        if spell.select_action in actions or selected_spell.spell_action is None:
            selected_spell.spell_action = spell.select_action
            break

def spell_cast_system(group: EntityGroup):
    controls: ControlComponent = group.query_singleton('controls').controls
    selected_spell: SelectedSpellComponent = group.query_singleton('selected_spell').selected_spell
    if "mouse_0_start" in controls.actions:
        selected_spell.spell_casting_start = controls.mouse_grid_position
    if "mouse_0_stop" in controls.actions:
        for spell_entity in group.query('spell'):
            spell: SpellComponent = spell_entity.spell
            if spell.select_action == selected_spell.spell_action:
                effect_direction = clamp_vector(controls.mouse_grid_position - selected_spell.spell_casting_start, Vector2(-1,-1), Vector2(1,1))
                effect_entity = create_effect(spell.effect, selected_spell.spell_casting_start, effect_direction)
                group.add(effect_entity)
                break
        selected_spell.spell_casting_start = None

def mount_spell_system(group: EntityGroup):
    spell_entity = Entity("spell")
    spell_entity.spell = SpellComponent(select_action="select_spell_1", effect="wave")

    selected_spell_entity = Entity("selected_spell")
    selected_spell_entity.selected_spell = SelectedSpellComponent()

    group.add(spell_entity)
    group.add(selected_spell_entity)

    group.mount_system(spell_select_system)
    group.mount_system(spell_cast_system)