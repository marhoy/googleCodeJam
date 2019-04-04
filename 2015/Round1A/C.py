import logging
import argparse
import fileinput

# Configure logging
logging.basicConfig(format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int(fo):
    string = fo.readline().strip()
    return int(string)


def get_float(fo):
    string = fo.readline().strip()
    return float(string)


def get_ints(fo):
    string = fo.readline().strip()
    return [int(s) for s in string.split()]


def get_string(fo):
    string = fo.readline().strip()
    return string


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
    from functools import reduce

    def _keep_left(hull, r):
        while len(hull) > 1 and ccw(hull[-2], hull[-1], r) >= 0:
            hull.pop()
        if not len(hull) or hull[-1] != r:
            hull.append(r)
        return hull

    points = sorted(points)
    l = reduce(_keep_left, points, [])
    u = reduce(_keep_left, reversed(points), [])

    return l.extend(u[i] for i in range(1, len(u) - 1)) or l


def main(fo):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        N = get_int(fo)
        points = [get_ints(fo) for _ in range(N)]

        output = []
        convex = convex_hull(points)
        for P in points:
            M = len(convex)
            if P in convex:
                M -= 1
            for Q in convex:
                if Q == P:
                    continue
                temp = 0
                for R in convex:
                    if R in [P, Q]:
                        continue
                    if ccw(P, Q, R) > 0:
                        temp += 1
                if temp < M:
                    M = temp
            output.append(M)

        print('Case #{}:'.format(case))
        for t in output:
            print(t)


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity. Can be repeated up to two times.")
    parser.add_argument('inputfile', nargs='?',
                        help="Read from file instead of stdin")
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose:
        if arguments.verbose == 1:
            logging.getLogger().setLevel(logging.INFO)
        if arguments.verbose >= 2:
            logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Run main(), with either a file or stdin as input source
    with fileinput.input(arguments.inputfile) as file:
        main(file)
