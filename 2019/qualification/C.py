import argparse
import functools
import logging
import sys

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


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    from itertools import tee
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def prime_list(numbers):
    import math

    primes = [0]
    for i, (a, b) in enumerate(pairwise(numbers)):
        if a == b:
            primes.append(0)
            continue
        first_prime = math.gcd(a, b)
        primes.append(first_prime)
        break

    # Calculate the rest of the primes by division
    for j in range(i+1, len(numbers)):
        primes.append(numbers[j] // primes[j])

    # Backtrack for the beginning of the list
    for j in range(i, -1, -1):
        primes[j] = numbers[j] // primes[j+1]

    return primes

# Idea:
# 1. It is sufficient to find a prime in the beginning of the list. The rest of the
#    primes can be calculated by division.
# 2. If the first two numbers are the same, continue until you find two unequal numbers.
#    Find the first prime by taking the greatest common divisor of those two numbers.
# 3. Calculate the beginning of the list by dividing in the other direction.


def main():
    import string

    cases = get_int()

    for case in range(1, cases + 1):
        N, L = get_ints()
        numbers = get_ints()

        # Reconstruct the list of primes
        list_of_primes = prime_list(numbers)

        # Make a set with all the unique primes
        primes_seen = set(list_of_primes)

        # Create a map from prime to character
        prime_to_c = {prime: char for char, prime in
                      zip(string.ascii_uppercase, sorted(list(primes_seen)))}

        LOG.debug("Decrypt dict: %s", prime_to_c)

        # Decrypt the message
        message = ''.join([prime_to_c[prime] for prime in list_of_primes])

        print('Case #{}: {}'.format(case, message))


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
