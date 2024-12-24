from collections import defaultdict, Counter
from functools import lru_cache

import numpy as np

numpad = np.array([
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"],
    ["X", "0", "A"],
])

movepad = np.array([
    ["X", "^", "A"],
    ["<", "v", ">"],
])


def parse_input(in_file):
    with open(in_file, "r") as fh:
        return [line.strip() for line in fh]


def move_to_num(from_button, to_button):
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


@lru_cache()
def move_to_dir(from_button, to_button):
    pos = tuple(np.argwhere(movepad == from_button)[0])
    target = tuple(np.argwhere(movepad == to_button)[0])
    X = tuple(np.argwhere(movepad == "X")[0])
    directions = ''

    # We prefer left/~up~ moves as those are the "furthest" on the move pad.
    # However, if these hit the X then we move down/right instead.
    # We strongly prefer moving the same direction as much as possible
    while pos != target:
        if pos[1] > target[1] and (pos[0], target[1]) != X:
            # Move left
            directions += "<" * (pos[1] - target[1])
            pos = (pos[0], target[1])
        elif pos[0] > target[0] and (target[0], pos[1]) != X:
            # Move up
            directions += "^" * (pos[0] - target[0])
            pos = (target[0], pos[1])
        elif pos[0] < target[0]:
            # Move down
            directions += "v" * (target[0] - pos[0])
            pos = (target[0], pos[1])
        elif pos[1] < target[1]:
            # Move right
            directions += ">" * (target[1] - pos[1])
            pos = (pos[0], target[1])
        else:
            raise ValueError("Failed to move correctly")

    return directions + "A"


def get_numpad_moves(code):
    presses = Counter()
    from_button = "A"
    for to_button in code:
        moves = move_to_num(from_button, to_button)
        from_button = to_button
        presses[moves] += 1
    return presses


def get_movepad_moves(presses):
    for press, cnt in dict(presses).items():
        presses[press] -= cnt
        from_button = "A"
        for to_button in press:
            directions = move_to_dir(from_button, to_button)
            presses[directions] += cnt
            from_button = to_button
    return presses


def part_1(codes, depth):
    total = 0
    for code in codes:
        presses = get_numpad_moves(code)
        for _ in range(depth):
            presses = get_movepad_moves(presses)

        complexity = sum(len(press) * cnt for press, cnt in presses.items())
        total += complexity * int(code[:3])

    return total


codes = parse_input("AoC_input/day21.txt")
print("Part.1: ", part_1(codes, depth=2))
print("Part.2: ", part_1(codes, depth=25))
