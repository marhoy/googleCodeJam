import bisect


def longdiv(divisor, divident):
    quotient, remainder = divmod(divisor, divident)
    return quotient, remainder/divident


def find_next_2_ext(number):
    idx = bisect.bisect_left(EXP_TABLE, number)
    return EXP_TABLE[idx]


def quicker_solution(n_stalls, k_people):
    integer, fraction = longdiv(n_stalls - k_people, find_next_2_ext(k_people + 1))
    min_dist = max_dist = integer
    if fraction >= 0.5:
        max_dist = integer + 1
    return max_dist, min_dist


if __name__ == '__main__':
    num_cases = int(input())

    EXP_TABLE = [2 ** i for i in range(61)]

    for case in range(1, num_cases + 1):
        N, K = map(int, input().split())
        large, small = quicker_solution(N, K)
        print("Case #{}: {} {}".format(case, large, small))
