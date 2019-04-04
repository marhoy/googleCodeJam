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
