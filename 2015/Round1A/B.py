import logging
import argparse
import fileinput

# Configure logging
logging.basicConfig(format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int(fo):
    string = fo.readline().strip()
    return int(string)


def get_float(fo):
    string = fo.readline().strip()
    return float(string)


def get_ints(fo):
    string = fo.readline().strip()
    return [int(s) for s in string.split()]


def get_string(fo):
    string = fo.readline().strip()
    return string


def people_seated(barbers, time):
    import math
    return sum([math.floor(time/barber) + 1 for barber in barbers])


def my_seated_time(barbers, my_position):
    import math
    low, high = -1, max(barbers)*my_position
    while high - low > 1:
        mid = math.floor((low + high)/2)
        # print(low, mid, high)
        if people_seated(barbers, mid) < my_position:
            low = mid
        else:
            high = mid
    return high


def main(fo):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        _, my_position = get_ints(fo)
        barbers = get_ints(fo)

        time = my_seated_time(barbers, my_position)
        my_position_at_t = my_position - people_seated(barbers, time - 1)

        for barber_id, barber_time in enumerate(barbers):
            if time % barber_time == 0:
                my_position_at_t -= 1
            if my_position_at_t == 0:
                break

        print('Case #{}: {}'.format(case, barber_id + 1))


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity. Can be repeated up to two times.")
    parser.add_argument('inputfile', nargs='?',
                        help="Read from file instead of stdin")
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose:
        if arguments.verbose == 1:
            logging.getLogger().setLevel(logging.INFO)
        if arguments.verbose >= 2:
            logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Run main(), with either a file or stdin as input source
    with fileinput.input(arguments.inputfile) as file:
        main(file)
