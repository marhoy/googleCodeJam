import sys
import math
import logging
logging.basicConfig(level=logging.ERROR)
LOG = logging.getLogger(__name__)


def getint():
    return int(input())


def getints():
    return [int(s) for s in input().split(" ")]


def init_field(area):
    # Make a list of all coordinates inside the smallest possible
    # rectangle with area >= requested_area
    field = list()
    i_max = int(math.ceil(math.sqrt(area)))
    j_max = int(math.ceil(area / i_max))
    for i in range(1, i_max + 1):
        for j in range(1, j_max + 1):
            cell = [i, j]
            field.append(cell)

    LOG.debug("Created a field of size %d*%d = %d", i_max, j_max, len(field))
    return i_max, j_max, field


def update_field(field, prepared_cell):
    # If the prepared cell in unprepared, remove it from the list of coordinates
    if prepared_cell in field:
        field.remove(prepared_cell)
        LOG.debug("Removed %s from %s", str(prepared_cell), str(field))
    return field


def find_target_cell(field, i_max, j_max):
    # Select the first non-prepared cell
    n = 0
    LOG.debug("Getting target cell %d from %s", n, str(field))
    i, j = field[n]

    # If the target is along the edge, move one cell towards the center.
    # By doing it this way, we fill in the edges "by mistake" (when Gopher digs in the wrong cell
    i = max(i, 2)
    i = min(i, i_max - 1)
    j = max(j, 2)
    j = min(j, j_max - 1)

    return [i, j]


def main():
    # Read in the number of cases
    cases = getint()

    for case in range(1, cases + 1):
        # Read in the requested number of cells to prepare
        requested_cells = getint()
        LOG.debug("Case %d: Requested number of cells: %d", case, requested_cells)

        # Create a new field
        i_max, j_max, field = init_field(requested_cells)

        for attempt in range(1001):  # We'll receive -1 -1 after 1001 tries

            LOG.debug("Getting ready to select cell from %s", str(field))
            target_cell = find_target_cell(field, i_max, j_max)

            # Ask Gopher to prepare a cell
            LOG.debug("Case %d: Attempt %d: Ask Gopher to prepare %s", case, attempt, str(target_cell))
            print(" ".join(map(str, target_cell)), flush=True)

            # Process the response
            response = getints()
            LOG.debug("Case %d: Got response %s", case, str(response))
            if response == [-1, -1]:
                LOG.error("Got -1 -1, field is %s", str(field))
                # We failed, just exit
                sys.exit(1)
            elif response == [0, 0]:
                # We solved this case! Break and continue with next case
                break
            else:
                # Update the field with the newly prepared cell
                field = update_field(field, response)

        LOG.warning("Case %d: Hit rate was %2.2f%%", case, requested_cells/attempt * 100)


if __name__ == '__main__':
    main()
