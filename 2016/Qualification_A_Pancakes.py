

def minimum_flips(pancakes):
    grouped_height = 1 + pancakes.count('-+') + pancakes.count('+-')
    if pancakes.endswith('-'):
        return grouped_height
    else:
        return grouped_height - 1


def flip(string):
    l = ['-' if c == '+' else '+' for c in string]
    return ''.join(l)


num_cases = int(input())

for case in range(1, num_cases + 1):
    string = input()
    orig_string = string

    flips = 0
    while True:
        i = string.rfind('-')
        if i < 0:
            break
        # print('\tFlipping at index', i)
        string = flip(string[:i+1]) + string[i+1:]
        flips += 1
        # print('\t', string)

    print("Case #{}: {}".format(case, flips))
