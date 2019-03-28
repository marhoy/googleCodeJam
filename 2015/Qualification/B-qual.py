import logging
import argparse
import sys

# Configure logging
logging.basicConfig(format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int(fo):
    string = fo.readline().strip()
    return int(string)


def get_float(fo):
    string = fo.readline().strip()
    return float(string)


def get_ints(fo):
    string = fo.readline().strip()
    return [int(s) for s in string.split()]


def get_string(fo):
    string = fo.readline().strip()
    return string


def main(fo=sys.stdin):
    import math

    cases = get_int(fo)

    # Idea: Loop over all possible smallest plate size x from 1 to max(plates)
    # If a plate contains more than x pancakes, it takes math.ceil(p / x) - 1
    # special minutes to reduce that plate to x pancakes.

    for case in range(1, cases + 1):
        D = get_int(fo)
        plates = get_ints(fo)
        best_solution = max(plates)
        for x in range(1, max(plates) + 1):
            special_minutes = 0
            for p in plates:
                special_minutes += math.ceil(p / x) - 1
            best_solution = min(best_solution, x + special_minutes)

        print('Case #{}: {}'.format(case, best_solution))


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity. Can be repeated up to two times.")
    parser.add_argument('-f', '--file', action='store',
                        help="Read from file instead of stdin")
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose:
        if arguments.verbose == 1:
            logging.getLogger().setLevel(logging.INFO)
        if arguments.verbose >= 2:
            logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Run main(), with either a file or stdin as input source
    if arguments.file is not None:
        with open(arguments.file) as file:
            main(fo=file)
    else:
        main()
