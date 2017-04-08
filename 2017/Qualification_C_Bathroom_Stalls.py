import logging
import numpy as np
import math

# Package-wide logging configuration
logging.basicConfig(format='%(levelname)s: %(module)s(%(lineno)s): %(message)s', level=logging.DEBUG)
LOG = logging.getLogger()


def find_best_stall(L_s, R_s):
    minimum = np.minimum(L_s, R_s)
    indices = np.argwhere(minimum == np.nanmax(minimum)).flatten()
    if indices.shape == (1, 1):
        return indices[0, 0]

    maximum = np.maximum(L_s[indices], R_s[indices])
    ind2 = np.argwhere(maximum == np.nanmax(maximum)).flatten()
    if ind2.shape != (1, 1):
        ind2 = ind2[0]

    return indices[ind2]


def find_L_R(stalls):
    L_s = np.empty(len(stalls))
    R_s = np.empty(len(stalls))
    L_s[:] = np.nan
    R_s[:] = np.nan

    for s in range(1, len(stalls) - 1):
        # print("considering this:", stalls)
        # LOG.debug(s, stalls[:s], stalls[s+1:])
        # print(s, stalls[:s], stalls[s+1:])
        if stalls[s] == 'o':
            L_s[s] = np.nan
            R_s[s] = np.nan
        else:
            L_s[s] = s - 1 - stalls[:s].rfind('o')
            R_s[s] = stalls[s + 1:].find('o')
            # print(L_s, R_s)
            # LOG.debug("L_s %o, R_s %o", L_s, R_s)

    return L_s, R_s


def slow_solution():
        print("Case %d, %d stalls, %d people", case, N, K)

        stalls = 'o' + '.'*N + 'o'

        # LOG.debug(stalls)
        # print(stalls)
        for k in range(K-1):
            L_s, R_s = find_L_R(stalls)
            s = find_best_stall(L_s, R_s)
            print(stalls, int(max(L_s[s], R_s[s])), int(min(L_s[s], R_s[s])))
            # print("Best stall: {}".format(s))
            stalls_list = list(stalls)
            stalls_list[s] = 'o'
            stalls = ''.join(stalls_list)

        # Time for the last person to take a seat:
        L_s, R_s = find_L_R(stalls)
        s = find_best_stall(L_s, R_s)

        stalls_list = list(stalls)
        stalls_list[s] = 'x'
        stalls = ''.join(stalls_list)
        print(stalls)


# After k people have sat down, there are N - k free seats
# The free seats are evenly distributed
# If an odd k number of people have sat down, there are at most N - k / (k+1) consecutive free seats
# If an even k number of people have sat down, the highest number of free consecutive seats are the same as if k was k-1


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
        print(k, large, small)
        if (large, small) == (0, 0):
            break
    return large, small


def quicker_solution(N, K):
    parts = math.ceil(math.log(K + 1, 2))
    number = (N - K) / 2 ** parts
    fraction = number - math.floor(number)
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
        LOG.info('Case #%d: N stalls: %d, K people: %d', case, N, K)

        large, small = quicker_solution(N, K)

        print("Case #{}: {:d} {:d}".format(case, large, small))
