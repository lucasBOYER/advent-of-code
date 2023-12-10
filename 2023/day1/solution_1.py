import re

RE_DIGIT = re.compile("\D")


def parse(line: str) -> int:
    digits = RE_DIGIT.sub("", line.strip("\n"))
    return int(digits[0] + digits[-1])


if __name__ == "__main__":
    with open("input.txt", "r") as stream:
        answer = sum([parse(line) for line in stream])
    print(answer)
