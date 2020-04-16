import argparse
import fileinput
import functools
import logging
from typing import List

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

# Configure logging
logging.basicConfig(
    format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int() -> int:
    """Read an int from file or stdin."""
    string = FILE.readline().strip()
    return int(string)


def get_float() -> float:
    """Read a float from file or stdin."""
    string = FILE.readline().strip()
    return float(string)


def get_ints() -> List[int]:
    """Read multiple ints from file or stdin."""
    string = FILE.readline().strip()
    return [int(s) for s in string.split()]


def get_string() -> str:
    """Read a string from file or stdin."""
    string = FILE.readline().strip()
    return string


def interest_level(floor: dict):
    """Calculate the interest level of the current floor."""
    level = sum(value for value in floor.values())
    return level


def initial_neighbours(floor: dict, rows: int, cols: int) -> dict:
    """Find all the inital neighbours."""
    all_neighbours = dict()
    for row in range(rows):
        for col in range(cols):
            cell_neigbours = dict()
            if col > 0:
                cell_neigbours["W"] = (row, col - 1)
            if col + 1 < cols:
                cell_neigbours["E"] = (row, col + 1)
            if row > 0:
                cell_neigbours["N"] = (row - 1, col)
            if row + 1 < rows:
                cell_neigbours["S"] = (row + 1, col)
            all_neighbours[(row, col)] = cell_neigbours
    return all_neighbours


def eliminate_and_update(to_eliminated: List, floor: dict, neighbours: dict) -> set:
    """Eliminate dancers and create list of dancers to check in next round."""
    LOG.info("Eliminating %d dancers", len(to_eliminated))

    to_be_checked = set()
    for pos in to_eliminated:
        LOG.debug("Eliminating pos: {}".format(pos))

        # Remove the person from the floor
        del floor[pos]

        # Update the neighbours of our neigbours
        to_west = neighbours[pos].get("W", None)
        to_east = neighbours[pos].get("E", None)
        to_north = neighbours[pos].get("N", None)
        to_south = neighbours[pos].get("S", None)
        if to_west:
            if to_east:
                neighbours[to_west]["E"] = to_east
            else:
                del neighbours[to_west]["E"]
        if to_east:
            if to_west:
                neighbours[to_east]["W"] = to_west
            else:
                del neighbours[to_east]["W"]
        if to_north:
            if to_south:
                neighbours[to_north]["S"] = to_south
            else:
                del neighbours[to_north]["S"]
        if to_south:
            if to_north:
                neighbours[to_south]["N"] = to_north
            else:
                del neighbours[to_south]["N"]

        # Add our neighbours to the check_list
        for neig in neighbours[pos].values():
            to_be_checked.add(neig)

        # Remove person from neighbours list
        del neighbours[pos]

    # No need to check persons that have been eliminated
    to_be_checked -= set(to_eliminated)

    return to_be_checked


def main():
    """This is where you write your solution."""
    cases = get_int()

    for case in range(1, cases + 1):
        # Read input data
        rows, cols = get_ints()

        # Store skill levels in a dictionary
        floor = dict()
        to_be_checked = []
        for row in range(rows):
            for col, value in enumerate(get_ints()):
                floor[(row, col)] = value
                to_be_checked.append((row, col))

        # Find initial neighbours, store in a dictionary
        neighbours = initial_neighbours(floor, rows, cols)

        # Interest level before any eliminations
        competition_interest = interest_level(floor)

        # Loop until competition is over
        n_rounds = 0
        while True:
            n_rounds += 1
            to_be_eliminated = []

            # Loop over the positions we need to check
            LOG.info("Need to check %s positions", len(to_be_checked))
            for pos in to_be_checked:
                if len(neighbours[pos]) == 0:
                    continue  # This dancer doesn't have any neighbours
                neig_values = [floor[neig] for neig in neighbours[pos].values()]
                if floor[pos] < (sum(neig_values) / len(neig_values)):
                    to_be_eliminated.append(pos)

            # Finished or not?
            if len(to_be_eliminated) == 0:
                break

            # Eliminate dancers and create new list to be checked
            to_be_checked = eliminate_and_update(to_be_eliminated, floor, neighbours)

            # Increase competition interest
            competition_interest += interest_level(floor)

            LOG.info("End of round %d: %d dancers left", n_rounds, len(floor))

        LOG.info("End of competition after %d rounds: %d dancers left",
                 n_rounds, len(floor))
        print('Case #{}: {}'.format(case, competition_interest))


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count', default=0,
                        help="Increase verbosity. "
                        "Can be repeated up to two times.")
    parser.add_argument('infile', default="-", nargs="?",
                        help="Read from file instead of stdin")
    arguments = parser.parse_args()

    # Possibly change logging level of the top-level logger
    if arguments.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    if arguments.verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)

    # Print debugging information
    LOG.debug("Finished parsing arguments: %s", arguments)

    # Define a global FILE variable (sys.stdin or infile) and run main()
    FILE = fileinput.input(files=arguments.infile)
    main()
