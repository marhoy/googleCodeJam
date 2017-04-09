import logging

# Package-wide logging configuration
logging.basicConfig(format='%(levelname)s: %(module)s(%(lineno)s): %(message)s', level=logging.INFO)
LOG = logging.getLogger()


def flip(string):
    l = ['-' if c == '+' else '+' for c in string]
    return ''.join(l)



# REview at attempt0 case 33
# Bug: Problem: -++++---+, K: 2 should be 6

if __name__ == "__main__":

    num_cases = int(input())
    LOG.info('Number of cases %d', num_cases)
    for case in range(1, num_cases + 1):
        string, K = input().split(' ')
        K = int(K)
        LOG.info('Case #%d: Problem: %s, K: %d', case, string, K)

        flips = 0
        while True:
            i = string.find('-')
            if i < 0:
                break
            if i+K > len(string):
                flips = "IMPOSSIBLE"
                break
            substr = string[i:i+K]
            string = string[:i] + flip(substr) + string[i+K:]
            flips += 1
            # print(flips, string)

        print("Case #{}: {}".format(case, flips))
