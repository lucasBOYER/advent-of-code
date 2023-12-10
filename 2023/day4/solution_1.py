def parse_line(line: str) -> int:
    card = line.split(":")[1]
    winning, mine = card.split("|")
    winning = set(winning.strip().replace("  ", " ").split(" "))
    mine = set(mine.strip().replace("  ", " ").split(" "))

    common = winning.intersection(mine)
    if len(common) == 0:
        return 0
    return 2 ** (len(common) - 1)


if __name__ == "__main__":
    s = 0
    with open("input.txt", "r") as stream:
        for line in stream:
            s += parse_line(line)
    print(s)
