import logging

# Package-wide logging configuration
logging.basicConfig(format='%(levelname)s: %(module)s(%(lineno)s): %(message)s', level=logging.INFO)
LOG = logging.getLogger()


def tidyness(string):
    tidy_index = string.count('-+') + string.count('+-')
    num_plusses = string.count('+')
    # print("In tidyness:", string, tidy_index, num_plusses)
    #if string.count('-') == len(string):
        # Unexplainable hack...
    #    tidy_index = tidy_index + 1
    return tidy_index, num_plusses


def flip(string):
    l = ['-' if c == '+' else '+' for c in string]
    return ''.join(l)


def find_best_index(string, K, seen_strings):
    best_tidy = len(string)
    best_num_plusses = 0
    best_idx = len(string)
    best_candidate = ''
    for i in range(len(string)-(K-1)):
        substr = string[i:i+K]
        # print(i, string[:i], substr, string[i+K:])
        candidate = string[:i] + flip(substr) + string[i+K:]
        tidy_number, num_plusses = tidyness(candidate)

        print(candidate, tidy_number, num_plusses, candidate.count('++') + candidate.count('--'))
        if (tidy_number < best_tidy) or ((tidy_number == best_tidy) and (num_plusses > best_num_plusses)):
            if candidate in seen_strings:
                continue
            best_tidy = tidy_number
            best_num_plusses = num_plusses
            best_idx = i
            best_candidate = candidate
    print("best_tidy", best_tidy, "best_plus", best_num_plusses)
    return best_idx, best_candidate, best_tidy

# REview at attempt0 case 33
# Bug: Problem: -++++---+, K: 2 should be 6

if __name__ == "__main__":

    num_cases = int(input())
    LOG.info('Number of cases %d', num_cases)
    for case in range(1, num_cases + 1):
        string, K = input().split(' ')
        K = int(K)
        LOG.info('Case #%d: Problem: %s, K: %d', case, string, K)

        seen_strings = [string]
        flips = 0
        while True:
            tidy_idx, num_plus = tidyness(string)
            if num_plus == len(string):
                break
            i, string, tidy_idx = find_best_index(string, K, seen_strings)
            flips += 1
            seen_strings.append(string)
            if flips > len(string)*10:
                # print("Flips: ", flips, "lenstr:", len(string)*10)
                flips = 'IMPOSSIBLE'
                break
            print(flips, i, string)

        print("Case #{}: {}".format(case, flips))
