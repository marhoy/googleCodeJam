import argparse
import functools
import logging
import sys

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

# Configure logging
logging.basicConfig(format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int():
    string = FILE.readline().strip()
    return int(string)


def get_float():
    string = FILE.readline().strip()
    return float(string)


def get_ints():
    string = FILE.readline().strip()
    return [int(s) for s in string.split()]


def get_string():
    string = FILE.readline().strip()
    return string


def find_all_neighbours(n_rows, n_columns):
    import itertools

    neighbours = dict()
    for row in range(n_rows):
        for col in range(n_columns):
            diagonals = [(r, c) for r, c in itertools.chain(
                zip(range(row + 1, n_rows), range(col + 1, n_columns)),
                zip(range(row - 1, -1, -1), range(col - 1, -1, -1)),
                zip(range(row + 1, n_rows), range(col - 1, -1, -1)),
                zip(range(row - 1, -1, -1), range(col + 1, n_columns))
            )]
            vert_hor = [(i, col) for i in range(n_rows)] + \
                       [(row, i) for i in range(n_columns)]
            neighbours[(row, col)] = set(diagonals + vert_hor) - {(row, col)}
    return neighbours


def main():
    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        R, C = get_ints()

        # For every point, find all neighbours that we are not allowed to move to
        neighbours = find_all_neighbours(R, C)

        # Make a list of the points we have visited
        visited = list()

        # Initialize current point
        point = (None, None)

        while neighbours:

            # Find the point with the most neighbours that we are allowed to move to
            next_point = max(neighbours,
                             key=lambda k: len(neighbours[k])
                             if point not in neighbours[k] else -1)
            if point in neighbours[next_point]:
                # If the best point is not allowed, then this case is impossible
                print('Case #{}: IMPOSSIBLE'.format(case))
                break

            # Else: We have identified our next point
            LOG.debug("Choosing %s with %i neighbours",
                      next_point, len(neighbours[next_point]))
            visited.append(next_point)

            # Remove the previous point from all the neighbour-sets, since we must no
            # longer count it as a possible neighbour
            for key in neighbours:
                neighbours[key] -= {point}

            # Remove the new point from the neighbours dict, so we don't visit it again
            del neighbours[next_point]

            # Update the current position
            point = next_point
        else:
            # We got through the whole grid, print the path we took
            print('Case #{}: POSSIBLE'.format(case))
            for p in visited:
                print(p[0] + 1, p[1] + 1)


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Increase verbosity. Can be repeated up to two times.")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="Read from file instead of stdin")
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    if arguments.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Define a global FILE variable (sys.stdin or infile) and run main()
    FILE = arguments.infile
    main()
