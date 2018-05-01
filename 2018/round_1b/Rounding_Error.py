import logging
import argparse
import sys
import math

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


def rounds_up(number):
    return round(number) == math.floor(number) + 1


def main(fh=sys.stdin):
    cases = get_int(fh)

    for case in range(1, cases + 1):
        LOG.info("Case %d", case)
        total_people, total_languages = get_ints(fh)
        responses = get_ints(fh)

        additional_people = total_people - sum(responses)
        responses = responses + [0]*additional_people
        initial_percentages = [response/total_people*100 for response in responses]
        additional_percent = 1/total_people*100

        LOG.info("Initial percentages: %s", initial_percentages)
        LOG.info("Addition people (percent per person): %d (%2.2f%%)", additional_people, additional_percent)

        additional_responses = {}
        for pos, percent in enumerate(initial_percentages):
            if rounds_up(percent):
                continue
            for i in range(1, additional_people + 1):
                if rounds_up(percent + i*additional_percent):
                    additional_responses[pos] = i
                    break
        if not additional_responses:
            # We couldn't make any number round up, just add all people to one response
            LOG.debug("Just adding all people to the first response")
            additional_responses[0] = additional_people

        LOG.info("Additional responses: %s", additional_responses)

        # Add people to the responses:
        people_remaining = additional_people
        for pos in sorted(additional_responses, key=additional_responses.get):
            if additional_responses[pos] <= people_remaining:
                responses[pos] += additional_responses[pos]
            people_remaining -= additional_responses[pos]
            if people_remaining == 0:
                break

        LOG.info("Updated responses: %s", responses)

        total_percentages = sum([round(response/total_people*100) for response in responses])
        print('Case #{}: {}'.format(case, total_percentages))


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
        main(fh=sys.stdin)
