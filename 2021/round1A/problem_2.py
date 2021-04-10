import argparse
import fileinput
import functools
import logging
import math
from typing import List

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)


def primes_up_to(n: int) -> List[int]:
    """Returns all prime numbers that are <= n."""
    out = list()
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            out.append(p)
            for i in range(p, n + 1, p):
                sieve[i] = False
    return out


ALL_PRIMES = primes_up_to(499)


def prime_factors(number: int) -> List[int]:
    """Find the prime factors of a number."""
    result = []

    # Try dividing by primes up to (and including) 499
    for i in reversed(ALL_PRIMES):
        # While number can be divided by i, do so.
        while number % i == 0:
            result.append(i)
            number = number // i
        # Are we finished?
        if number == 1:
            break

    # Condition if n is a prime number greater than 2
    if number > 2:
        result.append(number)

    return result


# Configure logging
logging.basicConfig(format="[%(lineno)03d]: %(message)s", level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int() -> int:
    """Read an int from file or stdin."""
    string = FILE.readline().strip()
    return int(string)


def get_float() -> float:
    """Read a float from file or stdin."""
    string = FILE.readline().strip()
    return float(string)


def get_ints() -> List[int]:
    """Read multiple ints from file or stdin."""
    string = FILE.readline().strip()
    return [int(s) for s in string.split()]


def get_string() -> str:
    """Read a string from file or stdin."""
    string = FILE.readline().strip()
    return string


def main():
    """This is where you write your solution."""
    from collections import Counter

    cases = get_int()

    for case in range(1, cases + 1):
        # Get input
        n_different_primes = get_int()
        cards = dict()
        for _ in range(n_different_primes):
            card, num = get_ints()
            cards[card] = num
        cards = Counter(cards)

        # Figure out the possible range of solutions to search
        n_cards = sum(cards.values())
        highest_card = max(cards)
        max_n_prod_cards = math.ceil(math.log(n_cards * highest_card, highest_card))
        max_prod_sum = highest_card * max_n_prod_cards
        total_sum = sum([value * num for value, num in cards.items()])
        min_sum = max(2, total_sum - max_prod_sum)

        # Check each possible solution
        candidates = []
        for target in range(min_sum, total_sum):
            factors = prime_factors(target)
            if factors[-1] > 499:
                continue

            c = cards.copy()
            c.subtract(factors)
            c_sum = sum([value * num for value, num in c.items()])

            if (min(c.values()) >= 0) and (c_sum == target):
                # We had the necessary cards for the factorization
                # And the sum of the remaining cards equals the target
                candidates.append(target)

        if len(candidates) == 0:
            answer = 0
        else:
            answer = max(candidates)

        print("Case #{}: {}".format(case, answer))


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Code Jam solution")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity. " "Can be repeated up to two times.",
    )
    parser.add_argument(
        "infile", default="-", nargs="?", help="Read from file instead of stdin"
    )
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    if arguments.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Define a global FILE variable (sys.stdin or infile) and run main()
    FILE = fileinput.input(files=arguments.infile)
    main()
