N_CUBES = {"red": 12, "green": 13, "blue": 14}


def parse_game(line: str) -> tuple:
    _game_id, _content = line.split(":")

    game_id = _game_id.split(" ")[1]
    content = _content.strip().strip("\n")
    results = content.split("; ")
    return int(game_id), [parse_result(r) for r in results]


def parse_result(set_result: str) -> dict:
    cubes = set_result.split(", ")
    combi = {}
    for c in cubes:
        count, color = c.split(" ")
        combi[color] = int(count)
    return combi


def verify_combi(combi: dict):
    return all([count <= N_CUBES[color] for color, count in combi.items()])


def parse_and_verify(line: str) -> tuple:
    game_id, results = parse_game(line)
    valid = all([verify_combi(combi) for combi in results])
    return game_id if valid else 0


if __name__ == "__main__":
    with open("input.txt", "r") as stream:
        print(sum([parse_and_verify(line) for line in stream]))
