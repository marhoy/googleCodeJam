import argparse
import collections
import fileinput
import functools
import logging
from typing import List, Set
import itertools

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


def is_valid_tower(tower: str) -> bool:
    chars = set(tower)
    grouped = [key for key in itertools.groupby(tower)]
    return len(chars) == len(grouped)


def middle_letters(tower: str) -> Set[str]:
    if len(set(tower)) <= 2:
        return set()
    else:
        grouped = [key for key, group in itertools.groupby(tower)]
        return set(grouped[1:-1])


def main():
    """This is where you write your solution."""
    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        _ = get_int()
        towers = get_string().split()

        # Check the start values
        if not all(is_valid_tower(tower) for tower in towers):
            print("Case #{}: {}".format(case, "IMPOSSIBLE"))
            continue

        # Check that middle letters doesn't occur multiple times
        most_common_middle = collections.Counter(
            itertools.chain.from_iterable([middle_letters(tower) for tower in towers])
        ).most_common(1)
        if most_common_middle and most_common_middle[0][1] > 1:
            print("Case #{}: {}".format(case, "IMPOSSIBLE"))
            continue

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
