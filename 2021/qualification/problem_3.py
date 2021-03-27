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


def find_factorization(N: int, cost: int) -> List[int]:
    """Find numbers that add up to the total cost."""
    factorization = []
    for i in range(N - 1):
        possible_cost = N - i
        min_remaining_cost = N - i - 2
        if cost >= possible_cost + min_remaining_cost:
            factorization.append(i)
            cost = cost - possible_cost
        else:
            cost -= 1
    return factorization


def solution(N: int, cost: int) -> str:
    """Find and order with specified cost."""
    max_cost = sum(range(2, N + 1))
    min_cost = N - 1
    if (cost < min_cost) or (cost > max_cost):
        return "IMPOSSIBLE"

    # Figure out how we can factorize the cost
    factorization = find_factorization(N, cost)

    # Start with sorted list and flip in reverse order
    data = list(range(1, N + 1))
    for i in range(N - 2, -1, -1):
        if i in factorization:
            data[i:] = reversed(data[i:])

    return " ".join(map(str, data))


def main():
    """This is where you write your solution."""
    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        N, cost = get_ints()
        print(f"Case #{case}: {solution(N, cost)}")


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
