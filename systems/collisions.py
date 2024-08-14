from engine.ecs import Entity, EntityGroup, enumerate_component, factory

from pygame import Vector2


'''
Component class to store decoded control inputs
'''
@enumerate_component("hitbox")
class HitboxComponent():
    radius_sq: float
    bounds: Vector2 = factory(Vector2)

    @staticmethod
    def from_box(size: tuple[int,int]) -> 'HitboxComponent':
        bounds = Vector2(size) / 2
        return HitboxComponent(
            radius_sq = bounds.length_squared(),
            bounds = bounds
        )


'''
Collision detection system:
Detect any entities in collision
'''
def update_collision_system(group: EntityGroup):
    
    # Sort by the leftmost positon (this makes sense later.)
    collidables = sorted(
        group.query("hitbox", "motion"),
        key = lambda e: e.motion.position.x - e.hitbox.bounds.x
        )

    # Do a sweep-and-prune search through the entities
    for i, a in enumerate(collidables):
        a_pos = a.motion.position
        a_bounds = a.hitbox.bounds
        rightmost = a_pos.x + a_bounds.x

        # Check all entities ahead of us
        for j in range(i + 1, len(collidables)):
            b = collidables[j]
            b_pos = b.motion.position
            b_bounds = b.hitbox.bounds
            leftmost = b_pos.x - b_bounds.x

            # No more collisions possible ahead of us. Prune this branch.
            if leftmost > rightmost:
                break

            # Ok. X axis overlaps. Does Y?
            y_overlap = a_pos.y - a_bounds.y < b_pos.y + b_bounds.y \
                    and a_pos.y + a_bounds.y > b_pos.y - b_bounds.y
            
            if y_overlap:
                # Bounding box checks pass.
                # Now what?
                print("overlap")



'''
Mounts the components and systems for reading controls
'''
def mount_collision_system(group: EntityGroup):
    group.mount_system(update_collision_system)
