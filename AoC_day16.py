import heapq
import numpy as np

from AoC_helpers import parse_input_str_array



def parse_input(in_file):
    arr = parse_input_str_array(in_file)
    start = tuple(np.argwhere(arr == "S")[0])
    end = tuple(np.argwhere(arr == "E")[0])
    maze = arr == "."
    maze[start] = True
    maze[end] = True
    return maze, start, end


def dijkstra(maze, start, end, penalty, find_route=True):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize scores
    scores = np.full(maze.shape, np.inf)
    scores[start] = 0

    pq = [(0, start, (0, 1))]
    parents = {start: []}

    while pq:
        score, pos, prev_dir = heapq.heappop(pq)

        # Try to step in each direction
        for dir in directions:
            new_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if maze[new_pos]:
                # Calculate direction change penalty
                turn_pen = penalty if dir != prev_dir else 0
                new_dist = score + 1 + turn_pen
                if new_dist < scores[new_pos]:
                    scores[new_pos] = new_dist
                    heapq.heappush(pq, (new_dist, new_pos, dir))
                    parents[new_pos] = [pos]
                elif new_dist == scores[new_pos]:
                    parents[new_pos].append(pos)
                elif (new_dist - penalty) == scores[new_pos] and maze[new_pos[0] + dir[0], new_pos[1] + dir[1]]:
                    parents[new_pos].append(pos)

    if scores[end] == np.inf:
        raise ValueError("No path found")

    squares = 0
    if find_route:
        def find_paths(pos, squares):
            squares.add(pos)
            for parent in parents[pos]:
                for _ in find_paths(parent, squares):
                    pass
            return squares

        squares = find_paths(end, set())
    return scores[end], squares


if __name__ == '__main__':
    maze, start, end = parse_input("AoC_input/day16.txt")
    score, squares = dijkstra(maze, start, end, 1000)
    #print("Part.1: ", score)
    print("Part.2: ", len(squares))


