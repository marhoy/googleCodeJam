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


def flip_pancakes(pancakes, where, width):
    selection = pancakes[where: where + width]
    flipped = ''.join(['-' if c == '+' else '+' for c in selection])
    return pancakes[:where] + flipped + pancakes[where + width:]


def main(fo):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        pancakes, K = fo.readline().split()
        K = int(K)

        flips = 0
        for i in range(len(pancakes) - K + 1):
            if pancakes[i] == '-':
                pancakes = flip_pancakes(pancakes, i, K)
                flips += 1

        if pancakes[-K:].count('-'):
            solution = 'IMPOSSIBLE'
        else:
            solution = flips

        print('Case #{}: {}'.format(case, solution))


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
