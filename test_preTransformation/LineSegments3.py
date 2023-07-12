# TODO: 제거

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class LineCode:
    def __init__(self, origin, destination):
        self.origin = np.array(origin)
        self.destination = np.array(destination)
        self.vector = self.destination - self.origin

def closest_points_on_two_lines(line1, line2):
    u = line1.vector
    v = line2.vector
    w = line1.origin - line2.origin

    a = np.dot(u, u)
    b = np.dot(u, v)
    c = np.dot(v, v)
    d = np.dot(u, w)
    e = np.dot(v, w)
    D = a * c - b * b

    if D < 1e-6:
        sc = 0.0
        tc = d / b if b > c else e / c
    else:
        sc = (b * e - c * d) / D
        tc = (a * e - b * d) / D

    point_on_line1 = line1.origin + sc * u
    point_on_line2 = line2.origin + tc * v

    return point_on_line1, point_on_line2

def calculate_midpoints(lines):
    points = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            p1, p2 = closest_points_on_two_lines(lines[i], lines[j])
            mid_point = (p1 + p2) / 2
            points.append(mid_point)
    return points

def plot_lines_and_points(lines, points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for line in lines:
        ax.plot([line.origin[0], line.destination[0]], [line.origin[1], line.destination[1]], [line.origin[2], line.destination[2]])

    points = np.array(points)
    ax.scatter(points[:,0], points[:,1], points[:,2], color='r')

    plt.show()

# example usage:

line1 = LineCode([0,0,0], [1,1,1])
line2 = LineCode([0,1,0], [1,0,1])
line3 = LineCode([0,0,1], [1,1,0])

lines = [line1, line2, line3]

points = calculate_midpoints(lines)
# plot_lines_and_points(lines, points)
print(points) 

# np.sum(points, axis=0) / len(points)

print(np.sum(points, axis=0))
