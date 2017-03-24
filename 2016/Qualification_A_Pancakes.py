

# input() reads a string with a line of input, stripping the '\n' (newline) at the end.
# This is all you need for most Google Code Jam problems.
num_cases = int(input())

for case in range(1, num_cases + 1):
    string = input()
    stack = [0 if c == '-' else 1 for c in string]

    grouped_height = 0
    for i in len(stack):

    print("Case #{}: {}".format(case, stack))
