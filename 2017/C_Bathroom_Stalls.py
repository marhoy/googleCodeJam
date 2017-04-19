import bisect
from collections import defaultdict
import math


def google_solution(N, K):
    S = {N}
    C = defaultdict(lambda: 0, {N: 1})
    P = 0
    while True:
        X = max(S)
        X0 = math.ceil((X - 1)/2)
        X1 = math.floor((X - 1)/2)
        P += C[X]
        print("X: {}, X0: {}, X1: {}\n\tP: {}".format(X, X0, X1, P))
        if P >= K:
            return X0, X1
        else:
            S.remove(X)
            S.add(X0)
            S.add(X1)
            C[X0] += C[X]
            C[X1] += C[X]
        print("\tS: {}\n\tC: {}".format(S, C.items()))


def longdiv(divisor, divident):
    quotient, remainder = divmod(divisor, divident)
    return quotient, remainder/divident


def find_next_2_exp(number):
    idx = bisect.bisect_left(EXP_TABLE, number)
    return EXP_TABLE[idx]


def quicker_solution(n_stalls, k_people):
    integer, fraction = longdiv(n_stalls - k_people, find_next_2_exp(k_people + 1))
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
        large2, small2 = google_solution(N, K)
        print("Case #{}: {} {}".format(case, large, small))
        print("Case #{}: {} {}".format(case, large2, small2))
