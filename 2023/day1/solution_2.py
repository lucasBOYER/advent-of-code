import re

RE_DIGIT = re.compile("\D")
DIGIT_MAP = {
    "one": "o1e",
    "two": "t2o",
    "three": "t3e",
    "four": "f4r",
    "five": "f5v",
    "six": "s6x",
    "seven": "s7n",
    "eight": "e8t",
    "nine": "n9e",
}


def substitute(line: str) -> str:
    for spelling, number in DIGIT_MAP.items():
        line = line.replace(spelling, str(number))
    return line


def parse(line: str) -> int:
    sub_with_digits = substitute(line.strip("\n"))
    digits = RE_DIGIT.sub("", sub_with_digits)
    return int(digits[0] + digits[-1])


if __name__ == "__main__":
    with open("input.txt", "r") as stream:
        answer = sum([parse(line) for line in stream])
    print(answer)
