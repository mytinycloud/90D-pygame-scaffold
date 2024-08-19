import random
from pygame import Rect, Vector2
from engine.ecs import Entity, EntityGroup, enumerate_component, factory
from systems.enemy import create_enemy
from systems.motion import Direction, MotionComponent
from systems.tilemap import TilemapComponent
from systems.turn import TurnComponent
from systems.ui import UIComponent
from systems.utils import round_vector


ENEMY_TYPES = {
    'mook': create_enemy((0, 0)),
    'boss': create_enemy((0, 0))
}


LEVELS = {
    1: {
        'spawn_area': (120, 120, 1, 16),
        'enemies': {
            'mook': 5,
            'boss': 1
        },
        'map_bounds': (16, 16)
    },
    2: {
        'spawn_area': (112, 112, 1, 32),
        'enemies': {
            'mook': 20,
            'boss': 4
        },
        'map_bounds': (32, 32)
    },
    3: {
        'spawn_area': (130, 150, 4, 4),
        'enemies': {
            'mook': 40,
            'boss': 8
        },
        'map_bounds': (64, 64)
    },
    4: {
        'spawn_area': (150, 150, 12, 12),
        'enemies': {
            'mook': 80,
            'boss': 16
        },
        'map_bounds': (128, 128)
    },
    5: {
        'spawn_area': (0, 0, 256, 256),
        'enemies': {
            'mook': 160,
            'boss': 32
        },
        'map_bounds': (256, 256)
    }
}

@enumerate_component('level')
class LevelComponent:
    current_level: int = 0
    levels: dict = factory(LEVELS)
    map: str = 'maps/map.png'


@enumerate_component('spawn')
class EnemySpawnComponent:
    enemy_type: str
    count: int = None
    interval: float = None
    last_spawned_turn: int = 0
    area: Rect = None

def level_progression_system(group: EntityGroup):
    enemy_entities = group.query('enemy')
    spawn_entities = group.query('spawn')
    level_entity = group.query_singleton('level', 'ui')
    level: LevelComponent = level_entity.level
    ui: UIComponent = level_entity.ui
    enemies = list(enemy_entities)
    spawns = list(spawn_entities)
    unspawned_enemies_count = sum([spawn.spawn.count for spawn in spawns])

    ui.text = f'Level {level.current_level}, enemies: {len(enemies)}, unspawned: {unspawned_enemies_count}'

    if len(enemies) <= 0 and unspawned_enemies_count <= 0:
        level.current_level += 1
        level_config = level.levels.get(level.current_level)
        if not level_config == None:
            map: TilemapComponent = group.query_singleton('tilemap').tilemap
            map.bounds = Rect(Vector2(len(map.map))/2 - Vector2(level_config['map_bounds']) / 2, level_config['map_bounds'])
            spawn_area = Rect(level_config['spawn_area'])
            for enemy_type, count in level_config['enemies'].items():
                spawn = Entity('spawn')
                spawn.spawn = EnemySpawnComponent(enemy_type=enemy_type, count=count, interval=5, area=spawn_area)
                spawn.motion = MotionComponent(position=spawn_area.topleft)
                group.add(spawn)
        else:
            print('Game Over. You win!')

def spawn_enemy_system(group: EntityGroup):
    turn: TurnComponent = group.query_singleton('turn').turn

    spawn_entities = group.query('spawn', 'motion')
    for spawn_entity in spawn_entities:
        spawn: EnemySpawnComponent = spawn_entity.spawn
        spawn_area = spawn.area

        if spawn.count <= 0:
            group.remove(spawn_entity)
            continue

        if turn.number - spawn.last_spawned_turn < spawn.interval:
            continue


        random_spawn = round_vector(Vector2(spawn_area.topleft) + Vector2(spawn_area.size) * random.random())
        spawn.last_spawned_turn = turn.number
        spawn.count -= 1
        enemy = ENEMY_TYPES.get(spawn.enemy_type).clone()
        enemy.motion.position = Vector2(random_spawn)
        group.add(enemy)
    

def mount_level_system(group: EntityGroup):
    level_entity = Entity('levels')
    level_entity.level = LevelComponent(levels=LEVELS)
    level_entity.ui = UIComponent(text='')
    level_entity.motion = MotionComponent(position=Vector2(10, 10))

    group.add(level_entity)

    group.mount_system(level_progression_system)
    group.mount_system(spawn_enemy_system)

