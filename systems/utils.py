from pygame import Vector2

'''
Converts the vector into an absolute form.
The second argument is true if this resulted in a rotation (instead of an inversion)
'''
def rectify_vector(v: Vector2) -> tuple[Vector2,bool]:
    if v.x < 0:
        if v.y < 0:
            return -v, False
        return Vector2(-v.x, v.y), True
    elif v.y < 0:
        return Vector2(v.x, -v.y), True
    return v, False

'''
Rotate a vector counter clockwise
'''
def rotate_vector_ccw(v: Vector2) -> Vector2:
    return Vector2(-v.y, v.x)

'''
Rotate a vector clockwise
'''
def rotate_vector_cw(v: Vector2) -> Vector2:
    return Vector2(v.y, -v.x)

'''
Compute the determinant of two vectors
'''
def determinant(a: Vector2, b: Vector2) -> float:
    return (a.x * b.y) - (a.y * b.x)

'''
Returns true if the point is left of the vector
'''
def is_left(v: Vector2, delta: Vector2) -> bool:
    return (v.x * delta.y) > (v.y * delta.x)

'''
Returns true if the vector V may project to the line defined by a1-a2
'''
def vector_projects_to(v: Vector2, a1: Vector2, a2: Vector2) -> True:
    return is_left(v, a1) != is_left(v, a2)

'''
Returns the intersection of two vectors va, vb.
vb is offset by delta. Intersection will be relative to va.
'''
def vector_intersection(va: Vector2, delta: Vector2, vb: Vector2) -> Vector2 | None:
    det = determinant(va, vb)
    
    if abs(det) < 1e-10:
        # Lines near parallel
        return None
    
    # Form line equations
    t = (delta.x * vb.y - delta.y * vb.x) / det
    u = (delta.x * va.y - delta.y * va.x) / det
    
    # Check if the intersection point lies on both line segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        return t * va
    return None