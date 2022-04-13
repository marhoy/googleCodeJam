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
    import random

    cases = get_int()

    for _ in range(1, cases + 1):
        n_rooms, max_moves = get_ints()
        weighted_sum, sum_of_weights = 0, 0
        moves = -1

        def add_room(n_exits, weight):
            nonlocal moves, weighted_sum, sum_of_weights
            moves += 1
            weighted_sum += n_exits * weight
            sum_of_weights += weight

        # Get the starting room
        room_id, n_exits = get_ints()
        add_room(n_exits, weight=1 / n_rooms)

        while moves < max_moves:
            print(f"T {random.randrange(1, n_rooms + 1)}")
            room_id, n_exits = get_ints()
            add_room(n_exits, weight=1 / n_rooms)

            if moves == max_moves:
                break

            print("W")
            room_id, n_exits = get_ints()
            add_room(n_exits, weight=1 / (n_rooms * n_exits))

        # Print estimate
        estimate = weighted_sum / sum_of_weights * n_rooms / 2
        print(f"E {int(estimate)}")


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
