import functools

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)


def main():
    """This is where you write your solution."""
    import sys
    import numpy as np

    cases = int(input())
    _ = int(input())

    # Read all results-data at once
    all_results = (
        np.fromfile(sys.stdin, dtype=np.int8).reshape(cases * 100, -1)[:, :10_000] - 48
    )

    for case in range(cases):
        players = all_results[case * 100 : (case + 1) * 100, :]

        # For the first test-set, you can actually get away with just:
        # cheater = np.argmax(players.mean(axis=1)) + 1

        question_difficulty = 1 - players.mean(axis=0)
        correct = np.dot(players, question_difficulty)
        wrong = np.dot(1 - players, 1 - question_difficulty)
        cheater = np.argmax(correct / wrong) + 1

        print(f"Case #{case + 1}: {cheater}")


if __name__ == "__main__":
    main()
