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


def transpose_list_of_strings(list_of_strings):
    """
    Transposes the input which is a list (iterable) of strings:
    Input: ['00001111', '00110011', '01010101']
    Output: ['000', '001', '010', '011', '100', '101', '110', '111']
    """
    return [''.join(digits) for digits in zip(*list_of_strings)]


def main():
    import math

    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        N, B, F = get_ints()

        bits_needed = math.ceil(math.log2(N))

        LOG.info("Case #%d: Testing N=%d machines (B=%d), using F=%d queries",
                 case, N, B, bits_needed)

        # Make test strings such that the columns correspond to the binary numbers
        # from 0 to N. We can maximally ask 5 times, so we cannot use more than 5
        # bits. We just discard any of the more significant bits. So for e.g. N = 35,
        # the value will just flip over: 0..31 0..2.
        # If N <= 16, we will send less than 5 test_strings.
        test_strings = transpose_list_of_strings(
            [bin(i)[2:].zfill(bits_needed)[-5:] for i in range(N)])

        # Send the test strings and store the received strings
        responses = []
        for test_string in test_strings:
            print(test_string)
            responses.append(get_string())

        # For the machines that work, we get back the same columns we sent.
        # So converting the columns to numbers, we would get 0..N if all machines worked
        # and we had enough bits. Remember that if N was > 31, the numbers flipped over.
        # So in N = 35 and machine 30 and 32 is broken, we get 0..29 31 1..2.
        ids_recv = [int(s, 2) for s in transpose_list_of_strings(responses)]

        broken_ids = [i for i in range(N) if i not in ids_recv]

        LOG.debug("IDs received: {}".format(ids_recv))
        LOG.info("Broken IDs: {}".format(broken_ids))

        # Send solution
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
