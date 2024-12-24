from collections import defaultdict, Counter
from functools import lru_cache

import numpy as np

numpad = np.array([
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["X", "0", "A"],
])

movepad = [
    ["X", "^", "A"],
    ["<", "v", ">"],
]

moves = {
    ("A", "A"): "A",
    ("A", "^"): "<A",
    ("A", ">"): "vA",
    ("A", "v"): "<vA",
    ("A", "<"): "v<<A",
    ("^", "A"): ">A",
    ("^", "^"): "A",
    ("^", ">"): "v>A",
    ("^", "<"): "v<A",
    ("^", "v"): "vA",
    ("v", "A"): "^>A",
    ("v", ">"): ">A",
    ("v", "v"): "A",
    ("v", "<"): "<A",
    ("v", "^"): "^A",
    (">", "A"): "^A",
    (">", "^"): "<^A",
    (">", "v"): "<A",
    (">", ">"): "A",
    (">", "<"): "<<A",
    ("<", "A"): ">>^A",
    ("<", "^"): ">^A",
    ("<", "v"): ">A",
    ("<", ">"): ">>A",
    ("<", "<"): "A",
}


def parse_input(in_file):
    with open(in_file, "r") as fh:
        return [line.strip() for line in fh]


def move_to_button(from_button, to_button):
    """If moving in the preferred direction would eventually move to the
    missing button, then move all the way in the 90° direction. """
    keypad = {'7': (0, 0), '8': (1, 0), '9': (2, 0),
              '4': (0, 1), '5': (1, 1), '6': (2, 1),
              '1': (0, 2), '2': (1, 2), '3': (2, 2),
              'x': (0, 3), '0': (1, 3), 'A': (2, 3)}

    x1, y1 = keypad[from_button]
    x2, y2 = keypad[to_button]
    nx, ny = keypad['x']  # missing button
    directions = ''
    while (x1, y1) != (x2, y2):
        if x2 < x1:  # highest priority is left
            if (y1 == ny) and (x2 == nx):  # if would move to missing button
                directions += '^' * (y1 - y2)  # move up instead
                y1 = y2
            else:
                directions += '<'
                x1 -= 1
        elif y2 < y1:  # move up
            directions += '^'
            y1 -= 1
        elif y2 > y1:
            if (x1 == nx) and (y2 == ny):  # if would move to missing button
                directions += '>' * (x2 - x1)  # move right instead
                x1 = x2
            else:
                directions += 'v'  # move down
                y1 += 1
        elif x2 > x1:  # lowest priority is right
            directions += '>'
            x1 += 1
    return directions


def move_to_button(from_button, to_button):
    pos = tuple(np.argwhere(numpad == from_button)[0])
    target = tuple(np.argwhere(numpad == to_button)[0])
    X = tuple(np.argwhere(numpad == "X")[0])
    directions = ''

    # We prefer left/down moves as those are the "furthest" on the move pad.
    # However, if these hit the X then we move up/right instead.
    # We strongly prefer moving the same direction as much as possible
    while pos != target:
        # If we need to go left we should, but not onto the X
        if pos[1] > target[1] and (pos[0], target[1]) != X:
            directions += "<" * (pos[1] - target[1])
            pos = (pos[0], target[1])
        # Otherwise we try to move up as much as we can
        elif pos[0] > target[0]:
            directions += "^" * (pos[0] - target[0])
            pos = (target[0], pos[1])
        # Next try down if we can, but not onto the X
        elif pos[0] < target[0] and (target[0], pos[1]) != X:
            directions += "v" * (target[0] - pos[0])
            pos = (target[0], pos[1])
        # Finally we'll move right
        else:
            directions += ">" * (target[1] - pos[1])
            pos = (pos[0], target[1])
    return directions + "A"


def get_numpad_moves(code):
    presses = Counter()
    from_button = "A"
    for to_button in code:
        moves = move_to_button(from_button, to_button)
        from_button = to_button
        presses[moves] += 1
    return presses


def dir_moves(presses):
    for press, cnt in dict(presses).items():
        presses[press] -= cnt
        presses += get_movepad_moves(press, cnt)
    return presses


@lru_cache
def get_movepad_moves(dirs, cnt):
    mv_presses = Counter()
    from_button = 'A'
    for to_button in dirs:
        directions = moves[(from_button, to_button)]
        from_button = to_button
        mv_presses[directions] += cnt
    return mv_presses


def part_1(codes, depth):
    total = 0
    for code in codes:
        presses = get_numpad_moves(code)
        for _ in range(depth):
            presses = dir_moves(presses)

        complexity = sum(len(press) * cnt for press, cnt in presses.items())
        total += complexity * int(code[:3])

    return total


codes = parse_input("AoC_input/day21.txt")
print("Part.1: ", part_1(codes, depth=2))
print("Part.2: ", part_1(codes, depth=25))
