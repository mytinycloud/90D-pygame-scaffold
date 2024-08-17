from init import init
from engine.window import Window
from engine.ecs import EntityGroup

import systems
import systems.enemy

# Build objects
window = Window()
group = EntityGroup()

# Load systems onto the group
# Note, systems will be run in the order they are mounted
systems.time.mount_time_system(group, window.clock)
systems.turn.mount_turn_system(group)
systems.controls.mount_control_system(group)
systems.player.mount_player_system(group)
systems.enemy.mount_enemy_system(group)
systems.effect.mount_effect_system(group)
systems.motion.mount_motion_system(group)
systems.testing.mount_testing_system(group)
systems.sprites.mount_sprite_system(group, window.surface)

# Game Initialization
init(group, window)

# Main loop
while not window.exited:
    window.handle_events()
    group.run_systems()
    window.update()

window.close()
