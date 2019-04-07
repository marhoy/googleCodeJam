import argparse
import logging
import sys

# Configure logging
logging.basicConfig(format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int():
    string = FILE.readline().strip()
    return int(string)


def get_float():
    string = FILE.readline().strip()
    return float(string)


def get_ints():
    string = FILE.readline().strip()
    return [int(s) for s in string.split()]


def get_string():
    string = FILE.readline().strip()
    return string


def main():
    cases = get_int()

    for case in range(1, cases + 1):

        # Your solution goes here

        print('Case #{}:'.format(case))


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Increase verbosity. Can be repeated up to two times.")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="Read from file instead of stdin")
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    if arguments.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Define a global FILE variable (sys.stdin or infile) and run main()
    FILE = arguments.infile
    main()
