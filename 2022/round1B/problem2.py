import argparse
import fileinput
import functools
import logging
from typing import List

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


def main():
    """This is where you write your solution."""
    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        N, P = get_ints()
        values = [get_ints() for _ in range(N)]

        last_inc, last_dec = 0, 0
        sol_inc, sol_dec = 0, 0

        for prods in values:
            this_min, this_max = min(prods), max(prods)
            this_change = this_max - this_min
            sol_inc_next = min(
                sol_inc + abs(last_inc - this_min) + this_change,
                sol_dec + abs(last_dec - this_min) + this_change,
            )
            sol_dec_next = min(
                sol_inc + abs(last_inc - this_max) + this_change,
                sol_dec + abs(last_dec - this_max) + this_change,
            )
            last_inc, last_dec = this_max, this_min
            sol_inc, sol_dec = sol_inc_next, sol_dec_next

        print("Case #{}: {}".format(case, min(sol_inc, sol_dec)))


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
