import logging
import argparse
import fileinput
from itertools import tee
import math

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


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def prime_list(numbers):
    # Reconstruct the list of prime numbers
    primes = []
    for a, b in pairwise(numbers):
        if a == b:
            primes.append(int(math.sqrt(a)))
        else:
            primes.append(math.gcd(a, b))

    # Add the first number
    primes.insert(0, int(numbers[0] / primes[0]))

    # Add last number
    primes.append(int(numbers[-1] / primes[-1]))

    return primes


def main(fo):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        N, L = get_ints(fo)
        numbers = get_ints(fo)

        # Reconstruct the list of primes
        list_of_primes = prime_list(numbers)

        # Make a set with all the unique primes
        primes_seen = set(list_of_primes)

        print("Number of unique primes:", len(primes_seen))

        # Create a map from prime to character
        import string
        prime_to_c = dict()
        for letter, prime in zip(string.ascii_uppercase, sorted(list(primes_seen))):
            prime_to_c[prime] = letter

        # Decrypt the message
        message = ''.join([prime_to_c[prime] for prime in list_of_primes])

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
