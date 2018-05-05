import logging
import argparse
import sys

# Configure logging
logging.basicConfig(format='[%(lineno)03d]: %(message)s', level=logging.WARNING)
LOG = logging.getLogger(__name__)


def get_int(fh):
    string = fh.readline().strip()
    return int(string)


def get_float(fh):
    string = fh.readline().strip()
    return float(string)


def get_ints(fh):
    string = fh.readline().strip()
    return [int(s) for s in string.split()]


def get_string(fh):
    string = fh.readline().strip()
    return string


def main(fh=sys.stdin):
    cases = get_int(fh)

    for case in range(1, cases + 1):

        customers = get_int(fh)
        lollipops = {i for i in range(customers)}
        counts = {}

        for customer in range(customers):
            num_flavors, *likes = get_ints(fh)

            LOG.debug("Customer likes %d flavors: %s", num_flavors, likes)

            # Update the table of likings
            for flavor in likes:
                counts[flavor] = counts.get(flavor, 0) + 1

            # Customer likes nothing
            if num_flavors == 0:
                print("-1", flush=True)
                continue

            # Customer likes one thing. Sell it if we have it.
            if num_flavors == 1:
                if likes[0] in lollipops:
                    print(likes[0], flush=True)
                    lollipops.remove(likes[0])
                else:
                    print("-1", flush=True)
                continue

            # Customer likes several things. Sell the least popular one of the ones we have.
            possibilities = lollipops.intersection(likes)
            LOG.debug("Possible sells: %s", possibilities)
            if not possibilities:
                # We didn't have any of them.
                print("-1", flush=True)
                continue
            for flavor in sorted(counts, key=counts.get):
                if flavor in possibilities:
                    print(flavor, flush=True)
                    lollipops.remove(flavor)
                    break


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

    # Run main(), with either a file or stdin as input source
    if arguments.file is not None:
        with open(arguments.file) as file:
            main(fh=file)
    else:
        main()
