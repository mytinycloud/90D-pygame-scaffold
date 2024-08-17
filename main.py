from engine.window import Window
from engine.ecs import EntityGroup

import systems

# Build objects
window = Window()
group = EntityGroup()

# Load systems onto the group
# Note, systems will be run in the order they are mounted
systems.time.mount_time_system(group, window.clock)
systems.turn.mount_turn_system(group)
systems.controls.mount_control_system(group)
systems.player.mount_player_system(group)
systems.motion.mount_motion_system(group)
systems.testing.mount_testing_system(group)
systems.sprites.mount_sprite_system(group, window.surface)

# Main loop
while not window.exited:
    window.handle_events()
    group.run_systems()
    window.update()

window.close()
