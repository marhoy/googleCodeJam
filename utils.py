import math
from itertools import starmap
from operator import mul


def ccw(a, b, c):
    """
    Each point a, b, c is a point in 2D represented by two coordinates (x, y).
    This function determines whether the turn from a->b to b->c is counter-clockwise.

    The function returns:
     > 0: If the turn is counter-clockwise
    == 0: If the three points are on a line
     < 0: If the turn is clockwise

    If ccw > 0, point c is to the left of the line from a->b
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])


def lines_intersect(a, b, c, d):
    """
    Each point a, b, c is a point in 2D represented by two coordinates (x, y).
    This function determines whether the line a-b intersects the line c-d.
    The intersection is not proper if e.g. point c is on the line a-b, or if the
    four points form a single line.

    The function returns:
     True: If the lines intersect
     False: IF the lines do not intersect properly
    """
    # Idea: Looking along a-b, c and d must be on different sides of that line.
    #  And, Looking along c-d, a and b must be on different sides of that line.
    if ccw(a, b, c) * ccw(a, b, d) > 0:
        return False
    if ccw(c, d, a) * ccw(c, d, b) > 0:
        return False
    return True


def convex_hull(points):
    """
    Given a list of points in 2D with coordinates (x, y).
    This function finds the points that make up the convex hull.

    The points are returned in order, starting from the leftmost point and
    going counter clockwise around the hull.

    Algorithm: Graham's Scan
    Complexity: O(n log n)
    """
    # Sort the points to find the leftmost point.
    # In a tie, the lowest point is selected.
    points = sorted(points)
    leftmost = points[0]

    # Sort the other points in increasing slope (y/x) from the lower leftmost point
    others = sorted(points[1:], key=lambda p: (p[1] - leftmost[1])/(p[0] - leftmost[0]))
    points = [leftmost] + others

    # Start from the leftmost point and work through all points.
    hull = []
    for p in points:
        # If we have to turn clockwise to reach this new point:
        #   pop points from the stack until we don't
        # else
        #   append this new point to the stack
        while len(hull) >= 2 and ccw(hull[-2], hull[-1], p) < 0:
            hull.pop()
        hull.append(p)

    return hull


def hull_area(points):
    """
    This function calculates the area of a hull, where the hull is described as a ordered polygon.
    The output from the "convex_hull(points)" should be well suited.

    The formula does not work if the points are not ordered.
    https://en.wikipedia.org/wiki/Shoelace_formula
    """
    n = len(points)
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area


def matrix_mul(A, B):
    """
    Matrix multiplication of two matrices A and B.
    The matrices are expressed as lists of lists, such that

    A = [[0, 1], [2, 3], [4, 5]

    corresponds to the matrix

         0  1
    A =  2  3
         4  5
    """
    return [[sum(starmap(mul, zip(row, col))) for col in zip(*B)] for row in A]


def rotation_matrix(roll, pitch, yaw):
    """
    This function returns a rotational matrix R, which can be used to rotate some points in 3D.
    The roll, pitch and yaw angle is specified in radians.

    For some points in a matrix A, the rotated points A' can them be calculated as:
    A' = matrix_mul(A, R)
    """

    def roll_matrix(angle):
        """
        Rotate around the
        """
        R = [
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]
        ]
        return R

    def pitch_matrix(angle):
        R = [
            [math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)]
        ]
        return R

    def yaw_matrix(angle):
        R = [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]
        ]
        return R

    R = matrix_mul(matrix_mul(yaw_matrix(yaw), pitch_matrix(pitch)), roll_matrix(roll))
    return R


def transpose(list_of_iterables):
    """
    Transposes the input which is a list of iterable:
    Input: ['00001111', '00110011', '01010101']
    Output: ['000', '001', '010', '011', '100', '101', '110', '111']

    Input: t = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    Output: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
    """
    if isinstance(list_of_iterables[0], str):
        return [''.join(digits) for digits in zip(*list_of_iterables)]
    if isinstance(list_of_iterables[0], (list, tuple)):
        return [[*digits] for digits in zip(*list_of_iterables)]


def factors(n: int) -> set:
    """
    Returns all unique factors of an integer n, not including 1 and n.
    So for a prime number, it will return an empty set.
    For 9, it will return {3}
    """
    from functools import reduce
    return set(reduce(list.__add__,
                      ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if
                       n % i == 0))) - {1, n}


def primes_up_to(n: int) -> list:
    """
    Returns all prime numbers that are <= n
    """
    out = list()
    sieve = [True] * (n+1)
    for p in range(2, n+1):
        if (sieve[p]):
            out.append(p)
            for i in range(p, n+1, p):
                sieve[i] = False
    return out
