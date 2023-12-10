import re
import numpy as np
from collections import namedtuple
from scipy.signal import convolve2d
from itertools import chain

RE_DIGIT = re.compile("([0-9]+)")
RE_SYMBOL = re.compile("[^a-zA-Z0-9\.\n]")
Digit = namedtuple("Digit", ["value", "span"])


def get_valid_cells(mask_array: np.ndarray) -> np.ndarray:
    """
    Using convultions to mark valid cells.
    2d conv with a 3x3 kernel filled with ones will count non-zeros
    mask values around.
    """
    conv_filter = np.ones((3, 3))
    valid_cells = convolve2d(mask_array, conv_filter, mode="same")
    valid_cells = (valid_cells > 0).astype(int)
    return valid_cells


def is_part_number(digit: Digit, valid_cells: np.ndarray, row_id: int) -> bool:
    return sum(valid_cells[row_id, digit.span[0] : digit.span[1]]) > 0


def get_part_numbers(
    digits_array: list[Digit], valid_cells: np.ndarray
) -> list[list[Digit]]:
    part_numbers = []
    for i, row in enumerate(digits_array):
        part_numbers.append([d for d in row if is_part_number(d, valid_cells, i)])
    return part_numbers


def is_star_neighbour(candidate: Digit, star_pos: np.ndarray) -> bool:
    # is neighbour iff infinity norm <= 1 for any of the point in span
    distances = [
        max(abs(np.array([star_pos[0], s]) - star_pos))
        for s in np.arange(*candidate.span)
    ]
    return any([d <= 1 for d in distances])


def get_sum_ratios(part_numbers: list[Digit], stars: list):
    s = 0
    for row, positions in enumerate(stars):
        candidates = list(
            chain(
                part_numbers[row],
                part_numbers[row - 1] if row - 1 >= 0 else [],
                part_numbers[row + 1] if row + 1 < len(part_numbers) else [],
            )
        )
        for p in positions:
            star_pos = np.array([row, p])
            neighbours = [c.value for c in candidates if is_star_neighbour(c, star_pos)]
            if len(neighbours) == 2:
                s += np.product(neighbours)
    return s


def parse_line(line) -> tuple[list[Digit], list[int], list[int]]:
    line = line.strip().strip("\n")
    shape = len(line)
    mask = [0] * shape
    stars = []

    digits = [
        Digit(int(match.group()), match.span()) for match in RE_DIGIT.finditer(line)
    ]

    for m in RE_SYMBOL.finditer(line):
        pos = m.span()[0]
        mask[pos] = 1
        if m.group() == "*":
            stars.append(pos)

    return digits, mask, stars


if __name__ == "__main__":
    with open("input.txt", "r") as stream:
        digits_array: list[dict] = []
        mask_array: list[list] = []
        stars_array: list[list] = []
        for line in stream:
            d, m, s = parse_line(line)
            digits_array.append(d)
            mask_array.append(m)
            stars_array.append(s)

        valid_cells = get_valid_cells(np.array(mask_array))
        part_numbers = get_part_numbers(digits_array, valid_cells)
        print(get_sum_ratios(part_numbers, stars_array))
