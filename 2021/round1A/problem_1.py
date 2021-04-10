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
        _ = get_int()
        numbers = get_ints()

        appended_digits = 0
        modified_numbers = numbers[:1]

        for number in numbers[1:]:

            target = modified_numbers[-1] + 1
            if number >= target:
                modified_numbers.append(number)
                continue

            length_difference = len(str(target)) - len(str(number))
            if number * 10 ** length_difference <= target:
                add_nines = int(str(number) + "9" * length_difference)
                if add_nines >= target:
                    modified_numbers.append(target)
                else:
                    length_difference += 1
                    modified_numbers.append(number * 10 ** length_difference)
            else:
                modified_numbers.append(number * 10 ** length_difference)

            appended_digits += length_difference

        print("Case #{}: {}".format(case, appended_digits))


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
