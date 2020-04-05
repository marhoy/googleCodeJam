import argparse
import fileinput
import functools
import logging
from typing import List

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

# Configure logging
logging.basicConfig(
    format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
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


class Person:
    """A person available for work."""

    def __init__(self, name: str):
        """Initialize a person with a name."""
        self.name = name
        self.available_at = 0

    def __repr__(self):
        """This is what a person looks like."""
        return "Name: {}, Available at: {}".format(
            self.name, self.available_at)


def work_order(task_list: List[List[int]], workforce: List[Person]) -> str:
    """Return work order of people."""
    # Initialize output
    output = ["Unkown"] * len(task_list)

    # Loop over the tasks sorted by start time.
    # Keep track of the original task index,
    # so we can ouput names in the correct order
    for task_idx, task in sorted(enumerate(task_list), key=lambda x: x[1][0]):
        start_time, end_time = task

        LOG.debug("Start time: {}".format(start_time))

        # Find a person that is available at this start time
        for person in workforce:
            if person.available_at <= start_time:
                person.available_at = end_time
                output[task_idx] = person.name
                break
        else:
            return("IMPOSSIBLE")

        LOG.debug(workforce)
    return "".join(output)


def main():
    """This is where you write your solution."""
    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        n_activities = get_int()

        # Get list of activities with start and end time
        activities = []
        for _ in range(n_activities):
            activities.append(get_ints())

        # Create a pool of workers
        people = [Person("C"), Person("J")]

        # Figure out the work order
        solution = work_order(activities, people)

        print('Case #{}: {}'.format(case, solution))


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
