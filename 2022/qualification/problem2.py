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
        # Get input
        from collections import defaultdict

        available = defaultdict(list)
        for _ in range(3):
            cmyk = get_ints()
            for key, value in zip("cmyk", cmyk):
                available[key].append(value)

        # Get the minimum for each printer
        for key, values in available.items():
            available[key] = min(values)

        # Sort colors in decreasing order
        available = {
            k: v
            for k, v in sorted(
                available.items(), key=lambda item: item[1], reverse=True
            )
        }

        # Select as much as possible until we have enough
        remaining = 1_000_000
        selected = dict()
        for key, value in available.items():
            use = min(value, remaining)
            remaining -= use
            selected[key] = use

        if remaining == 0:
            solution = " ".join(str(selected[key]) for key in "cmyk")
        else:
            solution = "IMPOSSIBLE"

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
