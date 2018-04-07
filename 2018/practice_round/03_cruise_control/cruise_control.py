def getint():
    return int(input())


def getints():
    return [int(s) for s in input().split(" ")]


def main():

    # Get the number of cases to process
    cases = getint()

    for case in range(1, cases + 1):
        # Get the distance to go and the number of other horses
        distance_to_go, num_other_horses = getints()

        # Make a list of the other horses. Each element is a list of two numbers: position and speed
        horses = list()
        for n in range(num_other_horses):
            horses.append(getints())

        # For each horse, calculate the time needed to reach position D
        times = []
        for horse in horses:
            time = (distance_to_go - horse[0]) / horse[1]
            times.append(time)

        # The maximum speed is given by the longest finish time of the other horses
        max_speed = distance_to_go / max(times)

        print("Case #{}: {}".format(case, max_speed))


if __name__ == '__main__':
    main()
