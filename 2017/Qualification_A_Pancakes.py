import logging

# Package-wide logging configuration
logging.basicConfig(format='%(levelname)s: %(module)s(%(lineno)s): %(message)s', level=logging.INFO)
LOG = logging.getLogger()

num_cases = int(input())
print('Number of cases %d', num_cases)


def is_tidy(string):
    for i, el in enumerate(string[1:]):
        if int(el) >= string[i-1]:
            return False
    return True


for case in range(1, num_cases + 1):
    number = input()
    LOG.info('Case #%d: Problem: %d', case, number)

    while True:
        if is_tidy(number):
            break
        else:
            number = number - 1

    print("Case #{}: {}".format(case, number))
