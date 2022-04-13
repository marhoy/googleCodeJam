import argparse
import fileinput
import functools
import logging
from typing import List

# Redefine the print function with flush=True. Needed for interactive problems.
print = functools.partial(print, flush=True)

# Configure logging
logging.basicConfig(format="[%(lineno)03d]: %(message)s", level=logging.WARNING)
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


def main():
    """This is where you write your solution."""
    import itertools

    def find_initiators(graph, used):
        return graph.keys() - graph.values() - used

    def find_paths(graph, values, start_nodes, used):
        paths = []
        for start in start_nodes:
            path, node = [], start
            while True:
                if node == 0 or node in used:
                    break
                path.append((node, values[node - 1]))
                node = graph[node]
            paths.append(path)
        return paths

    def find_best_path(paths):
        scores = {}
        for idx, path in enumerate(paths):
            path_values = [node[1] for node in path]
            scores[idx] = sum(value_rank[value] for value in path_values)
        best_idx = min(scores, key=scores.get)
        max_value = max([node[1] for node in paths[best_idx]])
        return paths[best_idx], max_value

    def run_path(path, used):
        for node, _ in path:
            used.add(node)

    cases = get_int()

    for case in range(1, cases + 1):
        # Your solution goes here
        _ = get_int()
        values = get_ints()
        links = get_ints()
        value_rank = {v: i for i, v in enumerate(sorted(values))}

        used = set()
        graph = {f: t for f, t in enumerate(links, start=1)}
        inits = find_initiators(graph, used)
        paths = find_paths(graph, values, inits, used)

        score = 0
        while True:
            if len(paths) == 0:
                break
            best_path, best_score = find_best_path(paths)
            score += best_score
            run_path(best_path, used)

            # Update start-points and shorten paths
            inits.remove(best_path[0][0])
            new_paths = []
            for path in paths:
                new_path = list(itertools.takewhile(lambda n: n[0] not in used, path))
                if len(new_path) > 0:
                    new_paths.append(new_path)
            paths = new_paths

        print("Case #{}: {}".format(case, score))


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Code Jam solution")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase verbosity. " "Can be repeated up to two times.",
    )
    parser.add_argument(
        "infile", default="-", nargs="?", help="Read from file instead of stdin"
    )
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
