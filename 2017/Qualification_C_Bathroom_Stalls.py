import logging
import math

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
LOG = logging.getLogger()


def quick_solution(N, K):
    segments = [N]
    for k in range(K):
        largest = max(segments)
        segments.remove(largest)
        new = (largest - 1)/2
        large = math.ceil(new)
        small = math.floor(new)
        segments.append(large)
        segments.append(small)
        LOG.debug("k: %d, Large: %d, Small: %d", k, large, small)
        if (large, small) == (0, 0):
            break
    return large, small


def longdiv(divisor, divident):
    quotient, remainder = divmod(divisor, divident)
    return quotient, remainder/divident


def ceil_log_2(number):
    for i in range(len(EXP_TABLE)):
        if number <= EXP_TABLE[i]:
            break
    return i


def quicker_solution(N, K):
    integer, fraction = longdiv(N - K, EXP_TABLE[ceil_log_2(K + 1)])
    LOG.debug("Integer: %d, Fraction: %f", integer, fraction)
    if fraction >= 0.5:
        large = integer + 1
    else:
        large = integer
    small = integer

    return large, small


if __name__ == '__main__':
    num_cases = int(input())
    LOG.info('Number of cases %d', num_cases)

    EXP_TABLE = [2 ** i for i in range(61)]

    for case in range(1, num_cases + 1):
        N, K = map(int, input().split())
        LOG.info('\n\nCase #%d: N stalls: %d, K people: %d', case, N, K)

        large, small = quick_solution(N, K)

        print("Case #{}: {} {}".format(case, large, small))
