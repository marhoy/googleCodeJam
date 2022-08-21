import argparse
import fileinput
import functools
import logging
from typing import List
import math

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

# Configure logging
logging.basicConfig(format="[%(lineno)03d]: %(message)s", level=logging.WARNING)
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


def squary_diff(values):
    sum_squares = sum(value**2 for value in values)
    squared_sum = sum(values) ** 2
    return sum_squares - squared_sum


def search_positive(values, max_val):
    for x in reversed(range(1, max_val + 1)):
        print("Testing", x)
        if squary_diff(values + [x]) == 0:
            return x
        if squary_diff(values + [x]) < 0:
            print("Became negative", values + [x])
            return "IMPOSSIBLE"
    return "IMPOSSIBLE"


def search_negative(values, min_val):
    for x in reversed(range(-1, min_val - 1, -1)):
        if squary_diff(values + [x]) == 0:
            return x
        if squary_diff(values + [x]) > 0:
            return "IMPOSSIBLE"
    return "IMPOSSIBLE"


def main():
    """This is where you write your solution."""
    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        N, K = get_ints()
        values = get_ints()

        initial = squary_diff(values)
        if initial > 0:
            solution = search_positive(values, int(math.sqrt(initial)))
        elif initial < 0:
            solution = search_negative(values, -int(math.sqrt(-initial)))
        else:
            solution = 0

        print("Case #{}: {}".format(case, solution))


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Code Jam solution")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity. " "Can be repeated up to two times.",
    )
    parser.add_argument(
        "infile", default="-", nargs="?", help="Read from file instead of stdin"
    )
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
