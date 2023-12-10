from collections import defaultdict
import numpy as np


def parse_game(line: str) -> tuple:
    _, _content = line.split(":")
    content = _content.strip().strip("\n")
    results = content.split("; ")
    accu = defaultdict(list)
    for r in results:
        accu = parse_result(r, accu)

    min_set = {color: max(records) for color, records in accu.items()}
    power = np.product(list(min_set.values()))
    return power


def parse_result(set_result: str, acc: dict) -> dict:
    cubes = set_result.split(", ")
    for c in cubes:
        count, color = c.split(" ")
        acc[color].append(int(count))
    return acc


if __name__ == "__main__":
    with open("input.txt", "r") as stream:
        print(sum([parse_game(line) for line in stream]))
