import logging
import argparse
import fileinput
from functools import lru_cache

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


@lru_cache()
def factors(n):
    """
    Returns all factors of n not including 1 and n
    """
    from functools import reduce

    return set(reduce(list.__add__,
                      ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if
                       n % i == 0))) - {1, n}


def list_from_pairs(prime_pairs):
    primes_list = []
    for i in range(len(prime_pairs)):
        if i == 0:
            # The first element is treated differently
            first = (prime_pairs[0] - prime_pairs[1])
            # The set was empty, because the same letter was repeated
            if not first:
                first = prime_pairs[0]
            primes_list.append(list(first)[0])
        else:
            j = i - 1
            common = prime_pairs[i].intersection(prime_pairs[j])
            if not common:
                common = prime_pairs[i]
            primes_list.append(list(common)[0])

    # The last element is also special
    last = prime_pairs[-1] - prime_pairs[-2]
    if not last:
        # The set was empty, because the same letter was repeated
        last = prime_pairs[-1]
    primes_list.append(list(last)[0])

    return primes_list


def main(fo):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        N, L = get_ints(fo)
        numbers = get_ints(fo)

        # Get the list of the prime pairs
        prime_pairs = [factors(n) for n in numbers]

        # Turn the pair-list into a list of primes (one for each character)
        primes_list = list_from_pairs(prime_pairs)

        # Make a set with all the unique primes
        primes_seen = set()
        for a in prime_pairs:
            primes_seen.update(a)

        # Create a map from prime to character
        import string
        prime_to_c = dict()
        for letter, prime in zip(string.ascii_uppercase, sorted(list(primes_seen))):
            prime_to_c[prime] = letter

        # Decrypt the message
        message = ''.join([prime_to_c[prime] for prime in primes_list])

        print('Case #{}: {}'.format(case, message))


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
