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


def main():
    import numpy as np

    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        P, Q = get_ints()

        intersections = np.zeros((Q + 1, Q + 1), int)
        for i in range(P):
            x, y, direction = FILE.readline().strip().split()
            x, y = int(x), int(y)
            if direction == 'N':
                intersections[:, y + 1:] += 1
            elif direction == 'S':
                intersections[:, :y] += 1
            elif direction == 'E':
                intersections[x + 1:, :] += 1
            elif direction == 'W':
                intersections[:x, :] += 1

        LOG.debug("{}".format(np.flipud(intersections.T)))
        LOG.debug("{}".format(np.argmax(intersections, axis=0)))
        LOG.debug("{}".format(np.argmax(intersections, axis=1)))

        min_x = np.argmax(intersections, axis=0)[0]
        min_y = np.argmax(intersections, axis=1)[0]

        print('Case #{}: {} {}'.format(case, min_x, min_y))


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
