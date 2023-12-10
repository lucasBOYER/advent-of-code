import numpy as np
import re
from functools import cache


RE_CARD_ID = re.compile("([0-9]+):")


def parse_line(line: str) -> tuple[int, int]:
    card_id = int(RE_CARD_ID.search(line).group(1))
    card = line.split(":")[1]

    winning, mine = card.split("|")
    winning = set(winning.strip().replace("  ", " ").split(" "))
    mine = set(mine.strip().replace("  ", " ").split(" "))

    common = winning.intersection(mine)
    return card_id, len(common)


if __name__ == "__main__":
    VALUES = {}
    with open("input.txt", "r") as stream:
        for line in stream:
            c_id, c_v = parse_line(line)
            VALUES[c_id] = c_v

    @cache
    def compute_score(card_id: int):
        score = VALUES[card_id]
        if score == 0:
            return 0
        next_cards = np.arange(card_id + 1, card_id + 1 + score)
        return score + sum([compute_score(c) for c in next_cards])

    solution = sum([compute_score(c) for c in VALUES.keys()]) + len(VALUES)
    print(solution)
