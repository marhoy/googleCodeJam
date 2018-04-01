import math
import sys


def getint():
    return int(input())


def getints():
    return [int(s) for s in input().split(" ")]


# Read in the number of cases
cases = getint()

for case in range(1, cases + 1):

    # Read in min, max and number of allowed guesses
    min_number, max_number = getints()
    max_guesses = getint()

    # Set the left and right boundaries
    left = min_number + 1  # Add one since the interval if open on left side
    right = max_number

    # Loop over the allowed number of guesses
    for guess in range(max_guesses):

        # Find the middle point
        middle = math.floor((left + right) / 2)

        # Guess the middle point and get the response
        print(middle, flush=True)
        response = input()

        # Update left and right boundaries
        if response == "WRONG_ANSWER":
            sys.exit(1)
        elif response == "TOO_SMALL":
            left = middle + 1
        elif response == "TOO_BIG":
            right = middle - 1
        elif response == "CORRECT":
            break
