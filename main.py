from engine.window import Window
from engine.ecs import EntityGroup

import systems

# Build objects
window = Window()
group = EntityGroup()

# Load systems onto the group
# Note, systems will be run in the order they are mounted
systems.controls.mount_control_system(group, window)
systems.player.mount_player_system(group)
systems.motion.mount_motion_system(group)
systems.sprites.mount_sprite_system(group, window)

# Main loop
while not window.exited:
    window.handle_events()
    group.run_systems()
    window.update()

window.close()
