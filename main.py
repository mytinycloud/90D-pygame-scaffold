from engine.window import Window
from engine.entity import EntityGroup, Entity

import systems

# Build objects
window = Window()
group = EntityGroup()

# Load systems onto the group
systems.sprites.mount_sprite_system(group, window)
systems.player.mount_player_system(group)

# Main loop
while not window.exited:
    window.handle_events()
    group.run_systems()
    window.update()

window.close()
