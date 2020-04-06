import math
from itertools import starmap
from operator import mul
from typing import List, Set


def binary_search(sorted_list, item):
    """Binary search a sorted list for an item.

    The function returns:
    - If the item is in the list: The index of the item
    - If the item is not in the list: None
    """
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = math.floor((low + high) / 2)
        guess = sorted_list[mid]
        if guess == item:
            return mid
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return None


def ccw(a, b, c):
    """Check if a turn is counter-clockwise.

    Each point a, b, c is a point in 2D represented by two coordinates (x, y).
    Determines whether the turn from a->b to b->c is counter-clockwise.

    The function returns:
     > 0: If the turn is counter-clockwise
    == 0: If the three points are on a line
     < 0: If the turn is clockwise

    If ccw > 0, point c is to the left of the line from a->b
    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])


def lines_intersect(a, b, c, d):
    """Check whether line a-b intersects line c-d.

    Each point a, b, c is a point in 2D represented by two coordinates (x, y).
    This function determines whether the line a-b intersects the line c-d.
    The intersection is not proper if e.g. point c is on the line a-b, or if
    the four points form a single line.

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


def point_in_polygon(point, polygon):
    """Check whether a point is inside a polygon.

    This implements a fast version of the winding number calculation,
    described here: http://geomalgorithms.com/a03-_inclusion.html

    Args:
        point: A point in 2D represented by coordinates (x, y)
        polygon: A list of points that make up the edges of the polygon.

    Returns:
        True if the point is inside the polygon.
        Points on the bottom and left edges counts as being inside,
        upper and right edge counts as outside.

    Examples:
        >>> polygon = [(0, 0), (0, 1), (1, 1), (1, 0)]
        >>> utils.point_in_polygon((0, 0.5), polygon)
        True
        >>> utils.point_in_polygon((0.5, 0), polygon)
        True
        >>> utils.point_in_polygon((1, 0.5), polygon)
        False
        >>> utils.point_in_polygon((.5, 1), polygon)
        False
    """
    # We need the polygon to be closed
    if not polygon[-1] == polygon[0]:
        polygon.append(polygon[0])

    winding_number = 0
    for edge in zip(polygon, polygon[1:]):
        # if edge crosses ray upwards and point is strictly left of edge
        if (edge[0][1] <= point[1] < edge[1][1])  \
                and (ccw(edge[0], point, edge[1]) < 0):
            winding_number += 1

        # if edge crosses ray downwards and point is strictly right of edge
        elif (edge[0][1] > point[1] >= edge[1][1]) \
                and (ccw(edge[0], point, edge[1]) > 0):
            winding_number -= 1

    # If winding number is 0, then point is outside the polygon
    return winding_number != 0


def convex_hull(points):
    """Return points on the convex hull.

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

    # Sort the other points in increasing slope (y/x) relative to the
    # lower leftmost point
    others = sorted(points[1:],
                    key=lambda p: (p[1] - leftmost[1]) / (p[0] - leftmost[0]))
    points = [leftmost] + others

    # Start from the leftmost point and work through all points.
    hull = []
    for point in points:
        # If we have to turn clockwise to reach this new point:
        #   pop points from the stack until we don't
        # else
        #   append this new point to the stack
        while len(hull) >= 2 and ccw(hull[-2], hull[-1], point) < 0:
            hull.pop()
        hull.append(point)

    return hull


def hull_area(points):
    """Calculate the area of a hull.

    This function calculates the area of a hull, where the hull is described
    as an ordered polygon. The output from the "convex_hull(points)" should
    be well suited.

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


def matrix_mul(a, b):
    """Matrix multiplication of two matrices A and B.

    The matrices are expressed as lists of lists, such that

    A = [[0, 1], [2, 3], [4, 5]

    corresponds to the matrix

         0  1
    A =  2  3
         4  5
    """
    return [[sum(starmap(mul, zip(row, col))) for col in zip(*b)] for row in a]


def rotation_matrix(roll, pitch, yaw):
    """Calculate rotation matrix.

    This function returns a rotational matrix R, which can be used to rotate
    some points in 3D. The roll, pitch and yaw angle is specified in radians.

    For some points in a matrix A, the rotated points A' can them be
    calculated as:
    A' = matrix_mul(A, R)
    """

    def roll_matrix(angle):
        r = [
            [1, 0, 0],
            [0, math.cos(angle), -math.sin(angle)],
            [0, math.sin(angle), math.cos(angle)]
        ]
        return r

    def pitch_matrix(angle):
        r = [
            [math.cos(angle), 0, math.sin(angle)],
            [0, 1, 0],
            [-math.sin(angle), 0, math.cos(angle)]
        ]
        return r

    def yaw_matrix(angle):
        r = [
            [math.cos(angle), -math.sin(angle), 0],
            [math.sin(angle), math.cos(angle), 0],
            [0, 0, 1]
        ]
        return r

    rotation = matrix_mul(matrix_mul(yaw_matrix(yaw),
                                     pitch_matrix(pitch)),
                          roll_matrix(roll))
    return rotation


def transpose(list_of_iterables):
    """Transpose a matrix (iterable of iterable).

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


def factors(n: int) -> Set[int]:
    """Factorize an integer.

    Returns all unique factors of an integer n, NOT including 1 and n.
    For 9, it will return {3}

    Args:
        n (int): The number to factories

    Returns:
        set: A set with the factors of n.

    Examples:
        >>> utils.factors(11)
        set()
        >>> utils.factors(12)
        {2, 3, 4, 6}
    """
    results = set()
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            results.add(i)
            results.add(n // i)
    return results - {1, n}


def primes_up_to(n: int) -> List[int]:
    """Returns all prime numbers that are <= n."""
    out = list()
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            out.append(p)
            for i in range(p, n + 1, p):
                sieve[i] = False
    return out
