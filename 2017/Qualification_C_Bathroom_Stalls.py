import logging
import math

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
LOG = logging.getLogger()


def quick_solution(N, K):
    segments = [N]
    for k in range(K):
        segments.sort(reverse=True)
        largest = segments.pop(0)
        new = (largest - 1)/2
        large = math.ceil(new)
        small = math.floor(new)
        segments.append(large)
        segments.append(small)
        LOG.debug("k: %d, Large: %d, Small: %d", k, large, small)
        if (large, small) == (0, 0):
            break
    return large, small


def quicker_solution(N, K):
    parts = math.ceil(math.log(K + 1, 2))
    number = (N - K) / 2 ** parts
    fraction = number - math.floor(number)
    LOG.debug("Parts: %d, Number: %f", parts, number)
    if fraction >= 0.5:
        large = math.ceil(number)
    else:
        large = math.floor(number)
    small = math.floor(number)

    return large, small


if __name__ == '__main__':
    num_cases = int(input())
    LOG.info('Number of cases %d', num_cases)

    for case in range(1, num_cases + 1):
        N, K = map(int, input().split())
        LOG.info('\n\nCase #%d: N stalls: %d, K people: %d', case, N, K)

        large, small = quicker_solution(N, K)

        print("Case #{}: {:d} {:d}".format(case, large, small))
