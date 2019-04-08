import argparse
import functools
import logging
import sys

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

# Configure logging
logging.basicConfig(format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int():
    string = FILE.readline().strip()
    return int(string)


def get_float():
    string = FILE.readline().strip()
    return float(string)


def get_ints():
    string = FILE.readline().strip()
    return [int(s) for s in string.split()]


def get_string():
    string = FILE.readline().strip()
    return string


def opposite(direction):
    if direction == 'E':
        return 'S'
    return 'E'


def move_pos(pos, direction):
    if direction == 'E':
        return pos[0], pos[1] + 1
    return pos[0] + 1, pos[1]


# Observation: If Lydias last move is an E, we need to stay above her track in order to
# avoid being boxed in. In that case, we want to move E until we hit the border, and then
# move S towards the corner. But we will sometimes we forced to move S if we're on Lydias
# track and she moved E. But her last move is E, so at some point she will have to
# go S, and then we can go E to get above her.

def main():
    import collections

    cases = get_int()

    for case in range(1, cases + 1):
        N = get_int()
        L = get_string()

        # Make a dict with Lydias positions and moves
        lydia = collections.OrderedDict()
        pos = (0, 0)
        for direction in L:
            lydia[pos] = direction
            pos = move_pos(pos, direction)

        # Our preferred direction
        preferred_direction = L[-1]

        # Make a dict with my position and moves
        me = collections.OrderedDict()

        pos = (0, 0)
        while not pos == (N - 1, N - 1):
            if lydia.get(pos, False):
                # Lydia has been here, making opposite move
                me[pos] = opposite(lydia[pos])
            elif max(pos) == N - 1:
                # We're on the edge, can't move in preferred direction
                me[pos] = opposite(preferred_direction)
            else:
                # Free to move in preferred direction
                me[pos] = preferred_direction

            # Update position
            pos = move_pos(pos, me[pos])

        print('Case #{}: {}'.format(case, ''.join(me.values())))


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Increase verbosity. Can be repeated up to two times.")
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="Read from file instead of stdin")
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    if arguments.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Define a global FILE variable (sys.stdin or infile) and run main()
    FILE = arguments.infile
    main()
