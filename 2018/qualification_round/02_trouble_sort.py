import logging
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


def getint():
    return int(input())


def getints():
    return [int(s) for s in input().split(" ")]


def trouble_sort(numbers):

    # Observation: Trouble sort is O(N^2), so it's a slow sorting algorithm.
    # For the large dataset, it is too slow.
    done = False
    while not done:
        done = True
        for i in range(len(numbers) - 2):
            if numbers[i] > numbers[i + 2]:
                done = False
                numbers[i:i + 3] = numbers[i:i + 3][::-1]

    return numbers


def fast_trouble_sort(numbers):
    import itertools

    # Observation: Trouble sort is comparing odd with odd and even with even.
    # And when switching, odd index'ed numbers stays as odd index'ed.
    # So we get the same result by sorting odd and even separately and then interleaving them.
    even = sorted(numbers[::2])
    odd = sorted(numbers[1::2])

    return [val for pair in itertools.zip_longest(even, odd) for val in pair if val is not None]


def check_sorted(numbers):
    for i in range(len(numbers) - 1):
        if numbers[i] > numbers[i + 1]:
            return i
    return 'OK'


def main():
    cases = getint()

    for case in range(1, cases + 1):
        _ = getint()
        numbers = getints()

        LOG.debug("Case %d: Before sort: %s", case, str(numbers))
        numbers = fast_trouble_sort(numbers)
        LOG.debug("Case %d: After sort: %s", case, str(numbers))

        sort_result = check_sorted(numbers)
        print("Case #{}: {}".format(case, sort_result))


if __name__ == '__main__':
    main()
