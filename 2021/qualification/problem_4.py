import argparse
import fileinput
import functools
import logging
from typing import List
import sys

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

# Configure logging
logging.basicConfig(format="[%(lineno)03d]: %(message)s", level=logging.WARNING)
logger = logging.getLogger(__name__)


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


def query_median(i: int, j: int, k: int) -> int:
    """Query the judge for the median."""
    print(f"{i} {j} {k}")
    result = get_int()
    if result == -1:
        print("We used too many queries...")
        sys.exit(1)
    return result


def send_answer(data: List[int]):
    """Send final answer to judge."""
    print(" ".join(map(str, data)))
    result = get_int()
    if result == -1:
        print("The answer was wrong...")
        sys.exit(1)


def find_solution(N):
    """Find the solution."""
    data = [2, 1]
    for i in range(3, N + 1):
        left_pos, right_pos, insert_point = 0, len(data) - 1, None
        while insert_point is None:
            median = query_median(data[left_pos], i, data[right_pos])
            if (median == data[left_pos]) and (left_pos == 0):
                # Append on left side
                insert_point = 0
            elif (median == data[right_pos]) and (right_pos == len(data) - 1):
                # Append on right side
                insert_point = len(data)
            else:
                # The insertion point is between left_pos and right_pos.
                # Use binary search to find insert_point.
                while insert_point is None:
                    logger.debug(
                        f"What to do? {i} goes between {data[left_pos]} and "
                        f"{data[right_pos]}: {data}"
                    )
                    candidate = (left_pos + right_pos) // 2

                    if candidate == left_pos:
                        # We have narrowed it down!
                        insert_point = left_pos + 1
                        break

                    median = query_median(data[candidate], i, data[right_pos])
                    if median == i:
                        left_pos = candidate
                    elif median == data[candidate]:
                        right_pos = candidate

        data.insert(insert_point, i)
    return data


def main():
    """This is where you write your solution."""
    cases, N, Q = get_ints()

    for case in range(1, cases + 1):
        solution = find_solution(N)
        send_answer(solution)


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
    logger.debug("Finished parsing arguments: %s", arguments)

    # Define a global FILE variable (sys.stdin or infile) and run main()
    FILE = fileinput.input(files=arguments.infile)
    main()
