import argparse
import fileinput
import functools
import logging
from typing import List

from scipy.special import comb

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

# Configure logging
logging.basicConfig(
    format='[%(lineno)03d]: %(message)s', level=logging.DEBUG)
LOG = logging.getLogger(__name__)


def get_int() -> int:
    """Read an int from file or stdin."""
    string = FILE.readline().strip()
    return int(string)


def get_float() -> float:
    """Read a float from file or stdin."""
    string = FILE.readline().strip()
    return float(string)


def get_ints() -> List[int]:
    """Read multiple ints from file or stdin."""
    string = FILE.readline().strip()
    return [int(s) for s in string.split()]


def get_string() -> str:
    """Read a string from file or stdin."""
    string = FILE.readline().strip()
    return string


def pascal(row: int, col: int) -> int:
    """Return the value of the Pascal triangle at a specific position.

    As Pascal's triangle have a lot of interesting features, the value
    at row, col happens to be "row choose col".
    """
    return int(comb(row, col))


def value_left_part(row, col):
    """Calculate the sum of the left part of a row, up until and including col."""
    return sum([pascal(row, c) for c in range(col + 1)])


def main():
    """Idea for solution.

    The largest numbers are in the middle of each row.
    We start by moving down the middle of each row, to increase the value fast.
    And we intend to end up along the left edge, where we can collect 1's until
    we're satisfied.

    As long as the left half (including the center) of the next row is not too much,
    we move down the center. Otherwise, if we can move one down and one to the left
    (keeping the column value), we do that. Otherwise, we move to the left on this row.
    """
    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        print('Case #{}:'.format(case))

        # Get the target value
        target = get_int()

        # Start on top of the pyramid
        row, col = (0, 0)
        value = 0
        n_steps = 0

        while target > value:
            print(row + 1, col + 1)
            value += pascal(row, col)

            n_steps += 1
            LOG.debug("Step %d: Added %d, current value %d" %
                      (n_steps, pascal(row, col), value))

            if (target - value) >= value_left_part(row + 1, (row + 1) // 2):
                LOG.debug("Moving down center")
                row += 1
                col = row // 2
            elif (target - value) >= value_left_part(row + 1, col) or (col == 0):
                LOG.debug("Moving diagonally")
                row += 1
            else:
                LOG.debug("Moving left")
                col -= 1


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Increase verbosity. "
                             "Can be repeated up to two times.")
    parser.add_argument('infile', default="-", nargs="?",
                        help="Read from file instead of stdin")
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    if arguments.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Define a global FILE variable (sys.stdin or infile) and run main()
    FILE = fileinput.input(files=arguments.infile)
    main()
