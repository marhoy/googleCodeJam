import logging
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)


def getint():
    return int(input())


def getints():
    return [int(s) for s in input().split(" ")]


def trouble_sort(numbers):
    done = False
    while not done:
        done = True
        for i in range(len(numbers) - 2):
            if numbers[i] > numbers[i + 2]:
                done = False
                numbers[i:i + 3] = numbers[i:i + 3][::-1]

    return numbers


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
        numbers = trouble_sort(numbers)
        LOG.debug("Case %d: After sort: %s", case, str(numbers))

        sort_result = check_sorted(numbers)
        print("Case #{}: {}".format(case, sort_result))


if __name__ == '__main__':
    main()
