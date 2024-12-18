import numpy as np

val_map = {
    ".": 0,
    "O": 1,
    "#": 2,
    "@": 3,
}

dir_map = {
    ">": (0, 1),
    "^": (-1, 0),
    "<": (0, -1),
    "v": (1, 0),
}


def parse_input(in_file):
    with open(in_file, "r") as fh:
        in_str = fh.read()

    out_map = []
    dirs = []
    for line in in_str.split('\n'):
        if line.startswith("#"):
            out_map.append([val_map[i] for i in line.strip()])
        else:
            dirs.extend([dir_map[i] for i in line.strip()])
    return np.array(out_map, dtype=int), dirs


def part_1(wmap, dirs):
    pos = tuple(np.argwhere(wmap == 3)[0])
    checksum = wmap.sum()
    for move in dirs:
        assert checksum == wmap.sum()
        new_pos = (pos[0] + move[0], pos[1] + move[1])
        if wmap[new_pos] == 2:
            # Hit a wall, move on
            continue
        elif wmap[new_pos] == 0:
            # Move to an empty space
            wmap[pos] = 0
            wmap[new_pos] = 3
            pos = new_pos
        elif wmap[new_pos] == 1:
            # There's a box, move along the line until we hit a space or a wall.
            line_end = new_pos
            while wmap[line_end] == 1:
                line_end = (line_end[0] + move[0], line_end[1] + move[1])
            if wmap[line_end] == 2:
                # We hit a wall while pushing so move on
                continue
            elif wmap[line_end] == 0:
                # We can push a box into an empty space
                wmap[line_end] = 1
                wmap[new_pos] = 3
                wmap[pos] = 0
                pos = new_pos

    return (np.where(wmap == 1)[0] * 100 + np.where(wmap == 1)[1]).sum()


val_map_pt2 = {
    ".": 0,
    "#": 2,
    "@": 3,
    "[": 4,
    "]": 5,
}


def parse_input_pt2(in_file):
    with open(in_file, "r") as fh:
        in_str = fh.read()

    out_map = []
    dirs = []
    for line in in_str.split('\n'):
        if line.startswith("#"):
            line = line.replace("#", "##")
            line = line.replace("O", "[]")
            line = line.replace(".", "..")
            line = line.replace("@", "@.")
            out_map.append([val_map_pt2[i] for i in line.strip()])
        else:
            dirs.extend([dir_map[i] for i in line.strip()])
    return np.array(out_map, dtype=int), dirs


def part_2(wmap, dirs):
    pos = tuple(np.argwhere(wmap == 3)[0])
    checksum = wmap.sum()
    for move in dirs:
        assert checksum == wmap.sum()
        new_pos = (pos[0] + move[0], pos[1] + move[1])
        if wmap[new_pos] == 2:
            # Hit a wall, move on
            continue
        elif wmap[new_pos] == 0:
            # Move to an empty space
            wmap[pos] = 0
            wmap[new_pos] = 3
            pos = new_pos
        elif wmap[new_pos] == 4 or wmap[new_pos] == 5:
            # There's a box, move along the line until we hit a space or a wall.
            if abs(move[1]) == 1:
                line_end = new_pos[1]
                while wmap[pos[0], line_end] == 4 or wmap[pos[0], line_end] == 5:
                    line_end += move[1]
                if wmap[pos[0], line_end] == 2:
                    # We hit a wall while pushing so do nothing
                    continue
                # We can push a box into an empty space
                if move[1] == 1:
                    wmap[pos[0], pos[1] + 1:line_end + 1] = wmap[pos[0], pos[1]:line_end]
                else:
                    wmap[pos[0], line_end:pos[1]] = wmap[pos[0], line_end + 1:pos[1] + 1]
                wmap[pos] = 0
                pos = new_pos
            else:
                print(wmap)
                row = pos[0]
                move_positions = [[pos[1]]]
                blocked = False
                while True:
                    new_mvs = []
                    row += move[0]
                    for i in move_positions[-1]:
                        if wmap[row, i] == 4:
                            new_mvs.append(i)
                            new_mvs.append(i + 1)
                        elif wmap[row, i] == 5:
                            new_mvs.append(i)
                            new_mvs.append(i - 1)
                        elif wmap[row, i] == 2:
                            blocked = True
                            break

                    if blocked:
                        break
                    elif new_mvs:
                        move_positions.append(set(new_mvs))
                    else:
                        # we're movin
                        while row != pos[0]:
                            spaces = move_positions.pop(-1)
                            for col in spaces:
                                wmap[row, col] = wmap[row-move[0], col]
                                wmap[row - move[0], col] = 0
                            row -= move[0]
                        pos = new_pos
                        break
        else:
            print(wmap[new_pos], wmap)
            raise NotImplementedError("Should never get here")

    return (np.where(wmap == 4)[0] * 100 + np.where(wmap == 4)[1]).sum()


in_file = "AoC_input/day15.txt"
# wmap, dirs = parse_input(in_file)
# print("Part.1: ", part_1(wmap, dirs))

wmap, dirs = parse_input_pt2(in_file)
print("Part.2: ", part_2(wmap, dirs))
