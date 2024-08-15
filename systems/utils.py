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
