import logging
import re

# Package-wide logging configuration
logging.basicConfig(format='%(levelname)s: %(module)s(%(lineno)s): %(message)s', level=logging.ERROR)
LOG = logging.getLogger()


# 111110 can be reduced to
# 100000 which results in
# 099999

# 2110 can be reduced to


def replace_function(matchobj):
    LOG.debug("replace got %s", matchobj)
    digit = matchobj.group(0)[0]
    replacement = digit + '0'*(len(matchobj.group(0)) - 1)
    LOG.debug("replacement %s", replacement)
    return replacement


def reduce_number(string):
    for i in range(1, 10):
        # Replace all substrings iiii with i000
        string = re.sub(str(i) + '{2,}', replace_function, string)
    return string


def replace_by_zeros(string):
    l = list(string)
    lowest = l[0]
    for i in range(1, len(l)):
        if l[i] < lowest:
            lowest = l[i]
            for j in range(i, len(l)):
                if l[j] > lowest:
                    l[j] = '0'
    return ''.join(l)


def is_tidy(string):
    LOG.info('Evaluating %s', string)
    if len(string) == 1:
        return True
    for i in range(len(string) - 1):
        LOG.debug("%s %s", string[i+1], string[i])
        if string[i+1] < string[i]:
            return False
    return True


def testing():
    string = '1112333455336735'
    print(string)
    string2 = reduce_number(string)
    print(string2)
    string3 = replace_by_zeros(string2)
    print(string3)
    import sys
    sys.exit(0)


if __name__ == '__main__':

    num_cases = int(input())
    LOG.info('Number of cases %d', num_cases)

    for case in range(1, num_cases + 1):
        number = int(input())
        LOG.info('Case #%d: Problem: %d', case, number)

        while True:
            if is_tidy(str(number)):
                break
            else:
                number = int(reduce_number(str(number)))
                number = int(replace_by_zeros(str(number)))
                number = number - 1

        print("Case #{}: {}".format(case, number))
