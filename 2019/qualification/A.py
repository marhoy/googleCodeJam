import logging
import argparse
import fileinput

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

# Idea: Start by setting A = N.
# If N contains 4 at the 1'th position, we want to subtract 1 from A.
# If N contains 4 at the 10'th position, we want to subtract 10 from A.
# Finally, calculate B as the difference between N and the new number A.


def main(fo):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        N = get_int(fo)
        A = N
        for i, digit in enumerate(reversed(str(N))):
            if digit == '4':
                A -= 10 ** i
        B = N - A
        print('Case #{}: {} {}'.format(case, A, B))


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity. Can be repeated up to two times.")
    parser.add_argument('inputfile', nargs='?',
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
    with fileinput.input(arguments.inputfile) as file:
        main(file)
