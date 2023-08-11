# TODO: 제거

import numpy as np

def find_midpoints(line1_origin, line1_vector, line2_origin, line2_vector):
    u = line1_vector
    v = line2_vector
    w = line1_origin - line2_origin

    a = np.dot(u, u)
    b = np.dot(u, v)
    c = np.dot(v, v)
    d = np.dot(u, w)
    e = np.dot(v, w)
    D = a * c - b * b

    if D < 1e-6:  # lines are almost parallel
        sc = 0.0
        tc = d / b if b > c else e / c
    else:
        sc = (b * e - c * d) / D
        tc = (a * e - b * d) / D

    # Closest point on line1 to line2
    pointOnLine1 = line1_origin + sc * u
    # Closest point on line2 to line1
    pointOnLine2 = line2_origin + tc * v

    return pointOnLine1, pointOnLine2


line1_origin = np.array([1, 2, -1])
line1_vector = np.array([-1, 0, 1]) - line1_origin

line2_origin = np.array([-1, 2, -1])
line2_vector = np.array([1, -2, 1]) - line2_origin

points = find_midpoints(line1_origin, line1_vector, line2_origin, line2_vector)
print(points)
