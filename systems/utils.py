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
Clamps a vector
'''
def clamp_vector(v: Vector2, min: Vector2, max: Vector2) -> Vector2:
    x,y = v.x,v.y
    if x < min.x:
        x = min.x
    elif x > max.x:
        x = max.x
    if y < min.y:
        y = min.y
    elif y > max.y:
        y = max.y
    return Vector2(x, y)

def round_vector(v: Vector2) -> Vector2:
    return Vector2(round(v.x), round(v.y))


def closest_cardinal(v: Vector2) -> Vector2:
    max_dot = -1
    max_v = None
    for cardinal in vector_cardinals(Vector2(0)):
        dot = cardinal * v
        if dot > max_dot:
            max_dot = dot
            max_v = cardinal
    return max_v
        

'''
Return the normal vectors for a given direction
'''
def vector_normals(pos: Vector2, diretion: Vector2) -> list[Vector2]:
    return (
        pos + rotate_vector_cw(diretion),
        pos + rotate_vector_ccw(diretion)
    )

'''
Return the 4 cardinal directions
'''
def vector_cardinals(pos: Vector2) -> list[Vector2]:
    return (
        pos + Vector2(1,0),
        pos + Vector2(0,1),
        pos + Vector2(-1,0),
        pos + Vector2(0,-1)
    )