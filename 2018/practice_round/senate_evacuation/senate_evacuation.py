
def getint():
    return int(input())


def getints():
    return [int(s) for s in input().split(" ")]


def remove_someone(parties):
    evacuated = ''

    # If there's only three people left, we can only evacuate one
    if list(parties.values()) == [1, 1, 1]:
        num_remove = 1
    else:
        num_remove = 2

    for _ in range(num_remove):
        # Get a list of parties sorted by people. Largest party first.
        keys = sorted(parties, key=parties.get, reverse=True)

        # If the dict is empty, return here
        if not keys:
            return evacuated, parties

        # Remove a person from the largest party. Add that person to the evacuation plan
        parties[keys[0]] -= 1
        evacuated += keys[0]

        # If that was the last person from that party: Remove that party from the dict.
        if parties[keys[0]] == 0:
            del parties[keys[0]]

    # Return the people to be evacuated and the updated dict of parties
    return evacuated, parties


def main():

    # Get the number of cases from standard input
    cases = getint()

    # Loop over each case
    for case in range(1, cases + 1):
        # Initialize output for this case
        plan = "Case #{}:".format(case)

        # Get the number of parties and the number of people in each party
        _ = getint()
        people = getints()

        # Create a dictionary with all the people. Keys: Name of party, Value: Number of people
        parties = dict()
        for i, p in enumerate(people):
            parties[chr(i + 65)] = p

        # Remove people and update the plan
        while parties:
            evac, parties = remove_someone(parties)
            plan += " {}".format(evac)

        # Finally, print the evacuation plan for this case
        print(plan + '\n')


if __name__ == '__main__':
    main()
