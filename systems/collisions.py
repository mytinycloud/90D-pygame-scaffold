from engine.ecs import Entity, EntityGroup, enumerate_component, factory
import dataclasses
from pygame import Vector2


@dataclasses.dataclass(init=True, slots=True)
class Intersection():
    overlap: Vector2
    other: Entity

SHAPE_BOX = 0
SHAPE_CIRCLE = 1
SHAPE_POINT = 2

'''
Component class to store hitbox information, and the resulting intersections.
'''
@enumerate_component("hitbox")
class HitboxComponent():
    bounds: Vector2 = factory(Vector2) # Bounding box for initial detection
    intersections: list[Intersection] = factory(list) # list of intersections to report
    layer_mask: int         # Layer mask that this hitbox exists on
    target_mask: int = 0    # Layer mask to record collisions from
    shape: int

    @staticmethod
    def from_box(size: tuple[int,int], layer: int) -> 'HitboxComponent':
        bounds = Vector2(size) / 2
        return HitboxComponent(
            bounds = bounds,
            layer_mask = layer,
            shape = SHAPE_BOX
        )

    @staticmethod
    def from_circle(diameter: int, layer: int) -> 'HitboxComponent':
        return HitboxComponent(
            bounds = Vector2(diameter/2),
            layer_mask = layer,
            shape = SHAPE_CIRCLE,
        )

    @staticmethod
    def from_point(layer: int) -> 'HitboxComponent':
        return HitboxComponent(
            bounds = Vector2(0),
            layer_mask = layer,
            shape = SHAPE_POINT,
        )

'''
Computes the overlap on a single dimension.
delta: the distance from a to b (ie, b.pos - a.pos)
bound: the combined widths (a.width + b.width)
Remember: the sign of the overlap will be the same as the sign of the delta.
'''
def _overlap(delta: float, bound: float) -> float:
    return (-bound if delta < 0 else bound) - delta

def _compute_intersection_box_box(a: Entity, b: Entity) -> Intersection:
    # Bounding box check is already passed, so we can guarantee that the collision has happened.
    delta = b.motion.position - a.motion.position
    bounds = a.hitbox.bounds + b.hitbox.bounds
    overlap_x = _overlap(delta.x, bounds.x)
    overlap_y = _overlap(delta.y, bounds.y)
    if abs(overlap_x) < abs(overlap_y):
        return Vector2(overlap_x, 0)
    return Vector2(0, overlap_y)

def _compute_intersection_circle_circle(a: Entity, b: Entity) -> Intersection | None:
    delta = b.motion.position - a.motion.position
    radius = a.hitbox.bounds.x + b.hitbox.bounds.x
    if delta.length_squared() >= radius * radius:
        return None
    return (delta.normalize() * radius) - delta

def _compute_intersection_box_circle(a: Entity, b: Entity) -> Intersection | None:
    delta = b.motion.position - a.motion.position
    box = a.hitbox.bounds

    # If a the circle center overlaps one axis, it reduces to a box-box check.
    # Note - this still expects the bounding box check already having passed.
    if abs(delta.x) <= box.x or abs(delta.y) <= box.y:
        return _compute_intersection_box_box(a, b)

    # Identify the box corner closest to the circle, and get the distance to that.
    delta.x -= -box.x if delta.x < 0 else box.x
    delta.y -= -box.y if delta.y < 0 else box.y

    # Effectively a circle-circle check to the closest point on the box
    radius = b.hitbox.bounds.x
    if delta.length_squared() >= radius * radius:
        return None
    return (delta.normalize() * radius) - delta


def _compute_intersection_circle_box(a: Entity, b: Entity) -> Intersection | None:
    overlap = _compute_intersection_box_circle(b, a)
    return -overlap if overlap != None else None

'''
Computes the intersection vector for two hitboxes.
The bounding box check is assumed to have already been done.
'''
def _compute_intersection(a: Entity, b: Entity) -> Intersection | None:

    # Note, box-point and circle-point can be treated as box-box and circle-circle
    # Because a point is equivalent to a zero width box or circle as required.

    a_shape = a.hitbox.shape
    b_shape = b.hitbox.shape

    if a_shape == SHAPE_BOX:
        if b_shape == SHAPE_CIRCLE:
            return _compute_intersection_box_circle(a, b)
        else: # SHAPE_BOX or SHAPE_POINT
            return _compute_intersection_box_box(a, b)
    elif a_shape == SHAPE_CIRCLE:
        if b_shape == SHAPE_BOX:
            return _compute_intersection_circle_box(a, b)
        else: # SHAPE_CIRCLE or SHAPE_POINT
            return _compute_intersection_circle_circle(a, b)
    else: # a_shape == SHAPE_POINT
        if b_shape == SHAPE_BOX:
            return _compute_intersection_box_box(a, b)
        elif b_shape == SHAPE_CIRCLE:
            return _compute_intersection_circle_circle(a, b)
        else: # b_shape == SHAPE_POINT
            # Shouldnt occurr. Points do not collide with points.
            return None



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
                overlap = _compute_intersection(a, b)

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
