import logging
import argparse
import fileinput
import re


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


def is_tidy(number):
    digits = str(number)
    for a, b in zip(digits[:], digits[1:]):
        if a > b:
            return False
    return True


def replace_function(matchobj):
    digit = matchobj.group(0)[0]
    replacement = digit + '0'*(len(matchobj.group(0)) - 1)
    return replacement


def reduce_number(number):
    # NOTE: This is not sufficient to solve the large problem...
    digits = str(number)
    for i in range(1, 10):
        # Replace all substrings iiii with i000
        digits = re.sub(str(i) + '{2,}', replace_function, digits)
    return int(digits)


def main(fo):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        N = get_int(fo)

        while not is_tidy(N):
            N -= 1

        print('Case #{}: {}'.format(case, N))


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
