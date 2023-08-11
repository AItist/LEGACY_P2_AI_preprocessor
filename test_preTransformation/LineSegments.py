# TODO: 제거

# class LineSegment:
#     def __init__(self, p1, p2):
#         self.p1 = p1
#         self.p2 = p2

#     def midpoint(self):
#         """Return the midpoint of the line segment."""
#         return self.interpolate(0.5)

#     def interpolate(self, t):
#         """Return a point on the line segment.
#         t is a float from 0 to 1, where 0 returns p1, and 1 returns p2.
#         """
#         x = self.p1[0] * (1 - t) + self.p2[0] * t
#         y = self.p1[1] * (1 - t) + self.p2[1] * t
#         z = self.p1[2] * (1 - t) + self.p2[2] * t
#         return (x, y, z)


# # Create two line segments
# line_segment1 = LineSegment((0, 0, 1), (5, 5, 1))
# line_segment2 = LineSegment((0, 5, 0), (5, 0, 0))

# # Find the midpoints of the two line segments
# midpoint1 = line_segment1.midpoint()
# midpoint2 = line_segment2.midpoint()

# # Create a line segment connecting the two midpoints
# midpoint_line_segment = LineSegment(midpoint1, midpoint2)

# # Find the midpoint of the line segment connecting the two midpoints
# overall_midpoint = midpoint_line_segment.midpoint()

# print(overall_midpoint)



import numpy as np

class LineSegment:
    def __init__(self, p1, p2):
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)

    def midpoint(self):
        """Return the midpoint of the line segment."""
        return self.interpolate(0.5)

    def interpolate(self, t):
        """Return a point on the line segment.
        t is a float from 0 to 1, where 0 returns p1, and 1 returns p2.
        """
        return self.p1 * (1 - t) + self.p2 * t

if __name__ == '__main__':
    # Create two line segments
    # line_segment1 = LineSegment((0, 0, 1), (5, 5, 1))
    # line_segment2 = LineSegment((0, 5, 0), (5, 0, 0))
    line_segment1 = LineSegment(np.array([0, 0, 1]), np.array([5, 5, 1]))
    line_segment2 = LineSegment(np.array([0, 5, 0]), np.array([5, 0, 0]))

    # Find the midpoints of the two line segments
    midpoint1 = line_segment1.midpoint()
    midpoint2 = line_segment2.midpoint()

    # Create a line segment connecting the two midpoints
    midpoint_line_segment = LineSegment(midpoint1, midpoint2)

    # Find the midpoint of the line segment connecting the two midpoints
    overall_midpoint = midpoint_line_segment.midpoint()

    print(overall_midpoint)
