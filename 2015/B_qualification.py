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
    import heapq

    cases = get_int(fo)

    for case in range(1, cases + 1):
        D = get_int(fo)
        plates = sorted(get_ints(fo), reverse=True)

        special_minutes = 0
        while True:
            try:
                largest, second_largest = plates[:2]
            except ValueError:
                largest = plates[0]
                second_largest = 0

            if largest > 1 + max(math.ceil(largest / 2), second_largest):
                largest = plates.pop(0)
                plates.append(math.ceil(largest/2))
                plates.append(math.floor(largest/2))
                plates.sort(reverse=True)
                special_minutes += 1
            else:
                break
        total_time = plates[0] + special_minutes
        print('Case #{}: {}'.format(case, total_time))


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
