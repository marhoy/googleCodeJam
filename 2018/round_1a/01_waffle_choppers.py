import logging
import argparse
import sys

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


def count_chips_per_row(waffle):
    chip_counts = []
    for row in waffle:
        chip_counts.append(row.count('@'))
    return chip_counts


def find_horizontal_cuts(waffle, n_h_cuts, target_per_cut):
    chip_count_per_row = count_chips_per_row(waffle)
    # Loop over the rows and find where to make horizontal cuts
    h_cuts = []
    count = 0
    for i, row_count in enumerate(chip_count_per_row):
        count += row_count
        if count == target_per_cut:
            # Make a horizontal cut here
            LOG.debug("Making a horizontal cut after row %d of %d", i, len(waffle))
            h_cuts.append(i)
            count = 0
            # Have we found enough cuts?
            if len(h_cuts) == n_h_cuts:
                return h_cuts
    # We didn't find sufficient horizontal cuts
    return False


def check_all_pieces(waffle, h_indexes, v_indexes, chips_per_piece):
    for i in range(len(h_indexes) - 1):
        LOG.debug("Selecting from row %d to %d", h_indexes[i], h_indexes[i + 1])
        for j in range(len(v_indexes) - 1):
            LOG.debug("Selecting from col %d to %d", v_indexes[j], v_indexes[j + 1])
            piece = ''
            for row in waffle[h_indexes[i]:h_indexes[i + 1]]:
                piece += row[v_indexes[j]:v_indexes[j + 1]]
            if not piece.count('@') == chips_per_piece:
                LOG.debug("%d is not %d", piece.count('@'), chips_per_piece)
                return False
    return True


def main(fo=sys.stdin):
    cases = get_int(fo)

    for case in range(1, cases + 1):
        n_rows, n_cols, n_h_cuts, n_v_cuts = get_ints(fo)

        waffle = []
        for row in range(n_rows):
            waffle.append(get_string(fo))

        LOG.debug("Case: %d, (%dx%d), Cuts: %dx%d", case, n_rows, n_cols, n_h_cuts, n_v_cuts)

        n_pieces = (n_h_cuts + 1) * (n_v_cuts + 1)
        chip_count_per_row = count_chips_per_row(waffle)

        # Is it possible to divide the chips evenly?
        if sum(chip_count_per_row) % n_pieces > 0:
            print("Case #{}: IMPOSSIBLE".format(case))
            continue

        chips_per_piece = sum(chip_count_per_row) / n_pieces
        LOG.debug("Case: %d: %d pieces, %d chips per piece", case, n_pieces, chips_per_piece)

        # Try to find horizontal cuts
        target_per_h_cut = chips_per_piece * (n_v_cuts + 1)
        h_cuts = find_horizontal_cuts(waffle, n_h_cuts, target_per_h_cut)
        if not h_cuts:
            print("Case #{}: IMPOSSIBLE".format(case))
            continue

        # Try to find vertical cuts
        LOG.debug("Case %d: Looking for vertical cuts", case)
        # noinspection PyPep8Naming,PyPep8Naming
        waffle_T = [''.join(s) for s in zip(*waffle)]
        target_per_v_cut = chips_per_piece * (n_h_cuts + 1)
        v_cuts = find_horizontal_cuts(waffle_T, n_v_cuts, target_per_v_cut)
        if not v_cuts:
            print("Case #{}: IMPOSSIBLE".format(case))
            continue

        h_indexes = [0] + [i + 1 for i in h_cuts] + [n_rows]
        v_indexes = [0] + [i + 1 for i in v_cuts] + [n_cols]

        all_equal = check_all_pieces(waffle, h_indexes, v_indexes, chips_per_piece)
        if all_equal:
            print("Case #{}: POSSIBLE".format(case))
        else:
            print("Case #{}: IMPOSSIBLE".format(case))


if __name__ == '__main__':

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Code Jam solution')
    parser.add_argument('-v', '--verbose', action='count',
                        help="Increase verbosity. Can be repeated up to two times.")
    parser.add_argument('-f', '--file', action='store',
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

    # Run main(), potentially with a file as the input source
    if arguments.file is not None:
        with open(arguments.file) as file:
            main(fo=file)
    else:
        main()
