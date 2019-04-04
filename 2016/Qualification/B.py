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


def flip_pancakes(pancakes: str, where: int) -> str:
    top = pancakes[:where]
    bottom = pancakes[where:]
    top = ''.join(['-' if c == '+' else '+' for c in top])
    pancakes = top[::-1] + bottom
    return pancakes


def main(fo):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        pancakes = get_string(fo)

        flips = 0
        # Start from the right side of the string and work towards left
        for i in range(len(pancakes), 0, -1):

            # If we find a '-', we need to flip at this index
            if pancakes[i - 1] == '-':

                # But if the left side starts with one or more '+'es, we must flip
                # the start of the string first
                if pancakes.startswith('+'):
                    j = pancakes.find('-')
                    pancakes = flip_pancakes(pancakes, j)
                    flips += 1

                pancakes = flip_pancakes(pancakes, i)
                flips += 1

        print('Case #{}: {}'.format(case, flips))


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
