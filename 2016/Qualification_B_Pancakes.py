import logging

# Package-wide logging configuration
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
LOG = logging.getLogger()


# Solution from Google...
def minimum_flips(pancakes):
    grouped_height = 1 + pancakes.count('-+') + pancakes.count('+-')
    if pancakes.endswith('-'):
        return grouped_height
    else:
        return grouped_height - 1


def flip(string):
    l = ['-' if c == '+' else '+' for c in string]
    return ''.join(reversed(l))


num_cases = int(input())

for case in range(1, num_cases + 1):
    string = input()
    orig_string = string
    LOG.info('Problem: %s', string)

    flips = 0
    while True:
        i = string.rfind('-')
        if i < 0:
            break

        part1 = string[:i+1]
        part2 = string[i+1:]
        LOG.debug('Part 1: %s, Part 2: %s', part1, part2)
        if part1.startswith('+'):
            i = part1.find('-')
            part1 = flip(part1[:i]) + part1[i:]
            flips += 1
            LOG.debug('New part1: %s', part1)
        string = flip(part1) + part2
        flips += 1
        LOG.info('After %d flips: %s', flips, string)

    print("Case #{}: {}".format(case, flips))
