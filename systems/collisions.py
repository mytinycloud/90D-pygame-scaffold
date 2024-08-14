from engine.ecs import Entity, EntityGroup, enumerate_component, factory
import dataclasses
from pygame import Vector2


@dataclasses.dataclass(init=True, slots=True)
class Intersection():
    overlap: Vector2
    other: Entity

'''
Component class to store hitbox information, and the resulting intersections.
'''
@enumerate_component("hitbox")
class HitboxComponent():
    radius_sq: float
    bounds: Vector2 = factory(Vector2) # Bounding box for initial detection
    intersections: list[Intersection] = factory(list) # list of intersections to report
    layer_mask: int         # Layer mask that this hitbox exists on
    target_mask: int = 0    # Layer mask to record collisions from
    is_circle: bool = False

    @staticmethod
    def from_box(size: tuple[int,int], layer: int) -> 'HitboxComponent':
        bounds = Vector2(size) / 2
        return HitboxComponent(
            radius_sq = bounds.length_squared(),
            bounds = bounds,
            layer_mask = layer,
        )
    
    @staticmethod
    def from_circle(radius: int, layer: int) -> 'HitboxComponent':
        return HitboxComponent(
            radius_sq = radius * radius,
            bounds = Vector2(radius),
            layer_mask = layer,
            is_circle = True
        )

def compute_intersection_box_box(a: Entity, b: Entity) -> Intersection:
    # Bounding box check is already passed, so we can guarantee that the collision has happened.
    delta = b.motion.position - a.motion.position
    return delta


def compute_intersection_circle_circle(a: Entity, b: Entity) -> Intersection | None:
    return None

def compute_intersection_box_circle(a: Entity, b: Entity) -> Intersection | None:
    return None

'''
Computers the intersection vector for two hitboxes.
The bounding box check is assumed to have already been done.
'''
def compute_intersection(a: Entity, b: Entity) -> Intersection | None:
    
    if a.hitbox.is_circle:
        if b.hitbox.is_circle:
            return compute_intersection_circle_circle(a, b)
        else:
            return -compute_intersection_box_circle(b, a)
    else:
        if b.hitbox.is_circle:
            return compute_intersection_box_circle(a, b)
        else:
            return compute_intersection_box_box(a, b)


'''
Collision detection system:
Detect any entities in collision, and add store them in the intersections mask
'''
def update_collision_system(group: EntityGroup):
    
    # Sort by the leftmost positon (this makes sense later.)
    collidables = sorted(
        group.query("hitbox", "motion"),
        key = lambda e: e.motion.position.x - e.hitbox.bounds.x
        )
    
    # Clear last ticks intersection information
    for e in collidables:
        if len(e.hitbox.intersections):
            e.hitbox.intersections.clear()

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
            if leftmost >= rightmost:
                break
            
            a_targets_b = a.hitbox.target_mask & b.hitbox.layer_mask
            b_targets_a = b.hitbox.target_mask & a.hitbox.layer_mask

            # If these objects dont consider each other as valid collision targets, then stop here.
            if not (a_targets_b or b_targets_a):
                continue

            # Ok. X axis overlaps. Does Y?
            y_overlap = a_pos.y - a_bounds.y < b_pos.y + b_bounds.y \
                    and a_pos.y + a_bounds.y > b_pos.y - b_bounds.y
            
            if y_overlap:
                # Bounding box checks pass. Do the work
                overlap = compute_intersection(a, b)

                if overlap != None:
                    
                    if a_targets_b:
                        a.hitbox.intersections.append(Intersection( overlap, b ))
                    if b_targets_a:
                        b.hitbox.intersections.append(Intersection( -overlap, a ))



'''
Mounts the components and systems for reading controls
'''
def mount_collision_system(group: EntityGroup):
    group.mount_system(update_collision_system)
