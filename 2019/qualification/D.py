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


def transpose(list_of_strings):
    """
    Transposes the input which is a list (iterable) of strings:
    Input: ['00001111', '00110011', '01010101']
    Output: ['000', '001', '010', '011', '100', '101', '110', '111']
    """
    return [''.join(digits) for digits in zip(*list_of_strings)]


def main():
    import math

    # Note: To test this locally, you would say:
    #
    # python interactive_runner.py python testing_tool.py 0 -- python D.py
    #
    # You can optionally add -v or -vv at the end to turn on info/debug messages

    cases = get_int()

    LOG.debug("Solving %i cases", cases)

    for case in range(1, cases + 1):
        N, B, F = get_ints()

        # After changing to the strategy of repeated-blocks-of-numbers, we only have
        # to require that the block size is larger than the number of broken machines.
        # If it wasn't, all machines in a block could be broken, and we wouldn't be
        # able to detect that a new block begins.
        # Since the maximum value for B is 15, we will never send more than 4 queries.
        bits_needed = math.ceil(math.log2(B + 1))

        LOG.info("Case #%d: Testing N=%i machines (B=%i, F=%i), using only %i queries",
                 case, N, B, F, bits_needed)

        # Make test strings such that the columns correspond to increasing binary numbers.
        # We are only going to ask "bits_needed" times (max 4), so we cannot
        # use more than "bits_needed" bits. We handle this by just discarding any
        # of the more significant bits.
        # So for e.g. N = 17 and 4 bits the values will just flip over: 0..15 0..2.
        test_strings = transpose(
            [bin(i)[2:].zfill(bits_needed)[-bits_needed:] for i in range(N)])

        LOG.debug("Will send the following test strings %s", test_strings)

        # Send the test strings and store the received strings
        responses = []
        for test_string in test_strings:
            print(test_string)
            responses.append(get_string())

        LOG.debug("Received the following response strings %s", responses)

        # For the machines that work, we get back the same columns that we sent.
        # So converting the received columns to numbers, we would get 0..N if all
        # machines worked and we had used enough bits.
        # But now, some of the columns (numbers) will be missing.
        # So if N = 35 and machine 30 and 32 is broken, we get 0..29 31 1..2.
        ids_recv = [int(s, 2) for s in transpose(responses)]

        # Now, we go through the numbers we received and transform them into
        # numbers from 0 to N. We need to keep track of which block we are in.
        block, machines_working = 0, []
        for i, d in enumerate(ids_recv):
            if i > 0 and d <= ids_recv[i - 1]:
                block += 1
            machines_working.append(block * 2 ** bits_needed + d)

        # Finally, the IDs of the broken machines are the numbers we did not receive
        broken_ids = [i for i in range(N) if i not in machines_working]

        LOG.debug("IDs received: %s", ids_recv)
        LOG.debug("Machines working: {}".format(machines_working))
        LOG.info("Broken IDs: {}".format(broken_ids))

        # Send solution and receive verdict
        print(' '.join(map(str, broken_ids)))
        verdict = get_int()

        # If the solution was incorrect, we exit with return value 1
        if not verdict == 1:
            sys.exit(1)


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
