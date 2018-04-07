import logging
logging.basicConfig(level=logging.WARNING)
LOG = logging.getLogger(__name__)


def getint():
    return int(input())


def get_input():
    chars = input().split(" ")
    return int(chars[0]), chars[1]


def robot_damage(program):
    damage = 0
    power = 1
    for char in program:
        if char == 'S':
            damage = damage + power
        if char == 'C':
            power = power * 2
    return damage


def reduce_damage(program):
    pos = program.rfind('CS')
    if pos == -1:
        # The program cannot be improved
        return None
    # We found an occurrence of 'CS', change it to 'SC'
    program_list = list(program)
    program_list[pos:pos + 2] = ['S', 'C']
    return "".join(program_list)


def main():
    cases = getint()

    for case in range(1, cases + 1):
        shield_strength, program = get_input()

        changes = 0
        LOG.debug("Case %d: After %d changes: %s has damage %d. Shield: %d",
                  case, changes, program, robot_damage(program), shield_strength)
        while robot_damage(program) > shield_strength:
            program = reduce_damage(program)
            if program is None:
                # Sorry, it was not possible to improve the program
                print("Case #{}: {}".format(case, 'IMPOSSIBLE'))
                break
            else:
                changes = changes + 1
                LOG.debug("Case %d: After %d changes: %s has damage %d. Shield: %d",
                          case, changes, program, robot_damage(program), shield_strength)
        else:
            # We didn't break out of the loop, so we found a solution
            print("Case #{}: {}".format(case, changes))


if __name__ == '__main__':
    main()
