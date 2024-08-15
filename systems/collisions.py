from engine.ecs import Entity, EntityGroup, enumerate_component, factory
from pygame import Vector2
import dataclasses
import typing
from . import utils


@dataclasses.dataclass(init=True, slots=True)
class Intersection():
    overlap: Vector2
    other: Entity

SHAPE_BOX = 0
SHAPE_CIRCLE = 1
SHAPE_POINT = 2
SHAPE_LINE = 3

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
    invert: bool = False

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
            shape = SHAPE_CIRCLE
        )

    @staticmethod
    def from_point(layer: int) -> 'HitboxComponent':
        return HitboxComponent(
            bounds = Vector2(0),
            layer_mask = layer,
            shape = SHAPE_POINT
        )
    
    @staticmethod
    def from_line(vector: tuple[int,int], layer: int) -> 'HitboxComponent':
        size, invert = utils.rectify_vector(Vector2(vector))
        return HitboxComponent(
            bounds = size / 2,
            layer_mask = layer,
            shape = SHAPE_LINE,
            invert = invert
        )
    
    def get_line_end(self) -> Vector2:
        if self.invert:
            return Vector2(self.bounds.x, -self.bounds.y)
        return self.bounds

'''
Computes the overlap on a single dimension.
delta: the distance from a to b (ie, b.pos - a.pos)
bound: the combined widths (a.width + b.width)
Remember: the sign of the overlap will be the same as the sign of the delta.
'''
def _overlap(delta: float, bound: float) -> float:
    return (-bound if delta < 0 else bound) - delta

def _overlap_box_point(bounds: Vector2, point: Vector2) -> Vector2:
    # Warning, this assumed bounding box check already passed - this just computes the overlap.
    overlap_x = _overlap(point.x, bounds.x)
    overlap_y = _overlap(point.y, bounds.y)
    if abs(overlap_x) < abs(overlap_y):
        return Vector2(overlap_x, 0)
    return Vector2(0, overlap_y)

def _overlap_circle_point(radius: float, point: Vector2) -> Vector2 | None:
    if point.length_squared() >= radius * radius:
        return None
    return (point.normalize() * radius) - point

'''
da: a_end from a_start
db: b_end from b_start
delta: b_start from a_start
'''
def _intersect_line_line(da: Vector2, delta: Vector2, db: Vector2) -> Vector2 | None:
    determinant = utils.determinant(da, db)
    
    if abs(determinant) < 1e-10:
        # Lines near parallel
        return None
    
    # Form line equations
    t = (delta.x * db.y - delta.y * db.x) / determinant
    u = (delta.x * da.y - delta.y * da.x) / determinant
    
    # Check if the intersection point lies on both line segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        intersect = t * da
        return intersect
    return None

def _compute_intersection_box_box(delta: Vector2, a: HitboxComponent, b: HitboxComponent) -> Vector2:
    return _overlap_box_point(a.bounds + b.bounds, delta)

def _compute_intersection_circle_circle(delta: Vector2, a: HitboxComponent, b: HitboxComponent) -> Vector2 | None:
    return _overlap_circle_point(a.bounds.x + b.bounds.x, delta)

def _compute_intersection_box_circle(delta: Vector2, a: HitboxComponent, b: HitboxComponent) -> Vector2 | None:
    box = a.bounds
    # If a the circle center overlaps one axis, it reduces to a box-box check.
    if abs(delta.x) <= box.x or abs(delta.y) <= box.y:
        return _overlap_box_point(a.bounds + b.bounds, delta)

    # Identify the box corner closest to the circle, and get the distance to that.
    delta.x -= -box.x if delta.x < 0 else box.x
    delta.y -= -box.y if delta.y < 0 else box.y
    return _overlap_circle_point(b.bounds.x, delta)

def _compute_intersection_box_line(delta: Vector2, a: HitboxComponent, b: HitboxComponent) -> Vector2 | None:
    return None

def _compute_intersection_circle_line(delta: Vector2, a: HitboxComponent, b: HitboxComponent) -> Vector2 | None:
    line = b.get_line_end()
    circle_span = utils.rotate_vector_cw(line).normalize() * a.bounds.x
    intersection = _intersect_line_line(circle_span, delta - line, line * 2)
    if not intersection:
        return None
    return circle_span - intersection

def _compute_intersection_line_line(delta: Vector2, a: HitboxComponent, b: HitboxComponent) -> Vector2 | None:
    da = a.get_line_end()
    db = b.get_line_end()
    intersection = _intersect_line_line(da * 2, delta - (db + da), db * 2)
    return Vector2(0) if intersection != None else None

'''
Reverses the signature of an intersection function.
Ie, box,circle to circle,box
'''
def _invert_intersection_fn( fn: typing.Callable[[Vector2, HitboxComponent,HitboxComponent], Vector2|None] ) -> typing.Callable[[Vector2, HitboxComponent,HitboxComponent], Vector2|None]:
    def inv_fn(delta: Vector2, a: HitboxComponent, b: HitboxComponent) -> Vector2 | None:
        overlap = fn(-delta, b, a)
        return -overlap if overlap != None else None
    return inv_fn

_compute_intersection_circle_box = _invert_intersection_fn(_compute_intersection_box_circle)
_compute_intersection_line_box = _invert_intersection_fn(_compute_intersection_box_line)
_compute_intersection_line_circle = _invert_intersection_fn(_compute_intersection_circle_line)

'''
Computes the intersection vector for two hitboxes.
The bounding box check is assumed to have already been done.
'''
def _compute_intersection(delta: Vector2, a: HitboxComponent, b: HitboxComponent) -> Vector2 | None:
    
    # Note, box-point and circle-point can be treated as box-box and circle-circle
    # Because a point is equivalent to a zero width box or circle as required.

    a_shape = a.shape
    b_shape = b.shape

    if a_shape == SHAPE_BOX:
        if b_shape == SHAPE_CIRCLE:
            return _compute_intersection_box_circle(delta, a, b)
        elif b_shape == SHAPE_LINE:
            return _compute_intersection_box_line(delta, a, b)
        else: # SHAPE_BOX or SHAPE_POINT
            return _compute_intersection_box_box(delta, a, b)
    elif a_shape == SHAPE_CIRCLE:
        if b_shape == SHAPE_BOX:
            return _compute_intersection_circle_box(delta, a, b)
        elif b_shape == SHAPE_LINE:
            return _compute_intersection_circle_line(delta, a, b)
        else: # SHAPE_CIRCLE or SHAPE_POINT
            return _compute_intersection_circle_circle(delta, a, b)
    elif a_shape == SHAPE_LINE:
        if b_shape == SHAPE_BOX:
            return _compute_intersection_line_box(delta, a, b)
        elif b_shape == SHAPE_CIRCLE:
            return _compute_intersection_line_circle(delta, a, b)
        elif b_shape == SHAPE_LINE:
            return _compute_intersection_line_line(delta, a, b)
        else: # SHAPE_POINT
            return None # Points do not collide with rays
    else: # a_shape == SHAPE_POINT
        if b_shape == SHAPE_BOX:
            return _compute_intersection_box_box(delta, a, b)
        elif b_shape == SHAPE_CIRCLE:
            return _compute_intersection_circle_circle(delta, a, b)
        else: # SHAPE_RAY or SHAPE_POINT
            # Shouldnt occurr. Points do not collide with points or rays.
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
                delta = b_pos - a_pos
                overlap = _compute_intersection(delta, a.hitbox, b.hitbox)

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
