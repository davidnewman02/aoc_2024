import numpy as np
from AoC_day16 import dijkstra

def parse_input(in_file, grid_size, count):
    maze = np.ones((grid_size+1, grid_size+1))
    with open(in_file, "r") as fh:
        for _, line in zip(range(count), fh):
            pos = line.strip().split(",")
            maze[int(pos[1]), int(pos[0])] = 0
    return maze

def get_pixels(in_file):
    pixels = []
    with open(in_file, "r") as fh:
        for line in fh:
            pos = line.strip().split(",")
            pixels.append((int(pos[1])+1, int(pos[0])+1))
    return pixels

def part_1(maze):
    end = int(maze.shape[0])
    maze = np.pad(maze, pad_width=1, mode='constant', constant_values=0)
    return dijkstra(maze, (1,1), (end, end), 0, False)


def part_2(pixels, grid_size):
    maze = np.ones((grid_size + 1, grid_size + 1))
    end = int(maze.shape[0])
    maze = np.pad(maze, pad_width=1, mode='constant', constant_values=0)
    for i, pixel in enumerate(pixels):
        maze[pixel] = 0
        # started with 1024 fro pt.1, needed to re-run a couple of times so picked something closer
        if i < 2870:
            continue
        try:
            dijkstra(maze, (1, 1), (end, end), 0, False)
        except Exception:
            # Input is off-by-one due to padding and backwards.
            return (pixel[1]-1, pixel[0]-1)
    return maze



input_ex = ("AoC_input/day18_ex.txt", 6, 12)
input_main = ("AoC_input/day18.txt", 70, 1024)
maze = parse_input(*input_main)
score, _ = part_1(maze)
print("Part.1: ", score)


pixels = get_pixels(input_main[0])
block = part_2(pixels, input_main[1])
print("Part.2: ", block)





