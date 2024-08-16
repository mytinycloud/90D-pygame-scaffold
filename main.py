from engine.window import Window
from engine.ecs import EntityGroup

import systems

# Build objects
window = Window()
group = EntityGroup()

# Load systems onto the group
# Note, systems will be run in the order they are mounted
systems.time.mount_time_system(group, window.clock)
systems.controls.mount_control_system(group)
systems.player.mount_player_system(group)
systems.aiming.mount_aiming_system(group)
systems.motion.mount_motion_system(group)
systems.collisions.mount_collision_system(group)
systems.lifetime.mount_lifetime_system(group)
systems.testing.mount_testing_system(group)
systems.sprites.mount_sprite_system(group, window.surface)

# Main loop
while not window.exited:
    window.handle_events()
    group.run_systems()
    window.update()

window.close()
