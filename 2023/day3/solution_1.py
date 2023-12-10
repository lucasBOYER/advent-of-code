import re
import numpy as np
from collections import namedtuple
from scipy.signal import convolve2d

RE_DIGIT = re.compile("([0-9]+)")
RE_SYMBOL = re.compile("[^a-zA-Z0-9\.\n]")

Digit = namedtuple("Digit", ["value", "span"])


def parse_line(line):
    line = line.strip().strip("\n")
    shape = len(line)
    mask = [0] * shape

    digits = [
        Digit(int(match.group()), match.span()) for match in RE_DIGIT.finditer(line)
    ]

    for m in RE_SYMBOL.finditer(line):
        mask[m.span()[0]] = 1

    return digits, mask


if __name__ == "__main__":
    with open("input.txt", "r") as stream:
        digits_array: list[dict] = []
        mask_array: list[list] = []
        for line in stream:
            d, m = parse_line(line)
            digits_array.append(d)
            mask_array.append(m)

        # using convultions to mark valid cells.
        # 2d conv with this kernel will count non-zeros mask values around
        mask_array = np.array(mask_array)
        conv_filter = np.ones((3, 3))
        valid_cells = convolve2d(mask_array, conv_filter, mode="same")
        valid_cells = (valid_cells > 0).astype(int)

        s = 0
        for i, row in enumerate(digits_array):
            for d in row:
                if sum(valid_cells[i, d.span[0] : d.span[1]]) > 0:
                    s += d.value
        print(s)
