import argparse
import functools
import logging
import sys
from functools import lru_cache

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

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


@lru_cache()
def longest_common(w1, w2):
    longest = 0
    i = -1
    LOG.debug("Checking words, %s and %s", w1, w2)
    while True:
        if -i > min(len(w1), len(w2)):
            break
        if w1[i] == w2[i]:
            longest += 1
            i -= 1
        else:
            break
    return longest


def main():
    import itertools

    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        n_words = get_int()
        words = []
        pairs = 0
        endings = []

        for i in range(n_words):
            words.append(get_string())

        while True:
            LOG.debug("Words: {}".format(words))
            longest = 0
            for w1, w2 in itertools.combinations(words, 2):
                candidate = longest_common(w1, w2)
                if candidate > longest and w1[-candidate:] not in endings:
                    LOG.debug("Found new best: %s and %s with length %s",
                              w1, w2, candidate)
                    best_pair = w1, w2
                    longest = candidate

            if longest >= 1:
                LOG.debug("Longest match with %s and %s: %d", best_pair[0], best_pair[1],
                          longest)
                LOG.debug("Removing %s and %s", best_pair[0], best_pair[1])
                words.remove(best_pair[0])
                words.remove(best_pair[1])
                endings.append(best_pair[0][-longest:])
                LOG.debug("Endings: {}".format(endings))
                pairs += 2
            else:
                break

        print('Case #{}: {}'.format(case, pairs))


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
