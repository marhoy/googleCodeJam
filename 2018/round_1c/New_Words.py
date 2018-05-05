import logging
import argparse
import sys
import itertools

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
    cases = get_int(fo)

    for case in range(1, cases + 1):
        words = set()
        num_words, word_length = get_ints(fo)
        for i in range(num_words):
            word = get_string(fo)
            words.add(word)

        LOG.debug("Case #%d: Words: %s", case, words)

        letters = []
        for i in range(word_length):
            letters.append({word[i] for word in words})

        for chars in itertools.product(*letters):
            word = ''.join(chars)
            if word not in words:
                solution = word
                break
            else:
                solution = "-"

        print('Case #{}: {}'.format(case, solution))


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
