import argparse
import fileinput
import functools
import logging
from typing import List, Tuple

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


def get_x_y_mural() -> Tuple[int, int, List[str]]:
    """Get all input."""
    string = FILE.readline().strip()
    xs, ys, mural = string.split()
    return int(xs), int(ys), list(mural)


def main():
    """This is where you write your solution."""
    cases = get_int()

    for case in range(1, cases + 1):
        X, Y, mural = get_x_y_mural()
        i, j = 0, 0
        while i < len(mural):
            if mural[i] != "?":
                i += 1
                continue
            # At this point, i is on a "?"
            j = i
            while (j < len(mural) - 1) and (mural[j + 1] == "?"):
                j += 1
            # ..and now, j is on the last "?" (possibly the same as i)

            # What characters are before and after the "?"s
            before = mural[i - 1] if i > 0 else None
            after = mural[j + 1] if j < len(mural) - 1 else None

            # What to fill with?
            fill = before if before is not None else after
            if fill is None:
                # Both before and after were None, just choose something
                fill = "J"

            # Fill missing characters
            mural[i : j + 1] = [fill] * (j - i + 1)

            # Move i forward
            i = j + 1

        mural = "".join(mural)
        cost = X * mural.count("CJ") + Y * mural.count("JC")

        print(f"Case #{case}: {cost}")


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
