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


def str_to_int(s):
    to_int = {'1': 1, 'i': 2, 'j':4, 'k': 8}
    if s.startswith('-'):
        return -to_int[s[1]]
    else:
        return to_int[s]


def int_to_str(i):
    to_str = {1: '1', 2: 'i', 4: 'j', 8: 'k'}
    if i < 0:
        return '-' + to_str[abs(i)]
    else:
        return to_str[i]


def times(a, b):
    import math
    mult = {
        1: {1: 1, 2: 2, 4: 4, 8: 8},
        2: {1: 2, 2: -1, 4: 8, 8: -4},
        4: {1: 4, 2: -8, 4: -1, 8: 2},
        8: {1: 8, 2: 4, 4: -2, 8: -1},
    }

    a = str_to_int(a)
    b = str_to_int(b)
    result = int(math.copysign(1, a) * math.copysign(1, b)) * mult[abs(a)][abs(b)]
    return int_to_str(result)


def check_total_product(string):
    string = list(string)
    c = string.pop(0)
    for c2 in string:
        c = times(c, c2)
    if c == '-1':
        return True
    else:
        return False


def check_parts(string):
    string = list(string)
    possible = False
    try:
        c = string.pop(0)
        while not c == 'i':
            c = times(c, string.pop(0))
        c = string.pop(0)
        while not c == 'j':
            c = times(c, string.pop(0))
        c = string.pop(0)
        while not c == 'k':
            c = times(c, string.pop(0))
    except IndexError:
        pass
    else:
        if len(string) == 0:
            possible = True

    return possible


def main(fo=sys.stdin):
    cases = get_int(fo)
    for case in range(1, cases + 1):
        L, X = get_ints(fo)
        string = get_string(fo)
        string = string * X

        if check_total_product(string) & check_parts(string):
            answer = 'YES'
        else:
            answer = 'NO'

        print('Case #{}: {}'.format(case, answer))


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
