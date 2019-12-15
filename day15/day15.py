from collections import namedtuple
from enum import IntEnum
from intcode import *
import sys

class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class Output(IntEnum):
    WALL = 0
    MOVED = 1
    OXYGEN = 2

Point = namedtuple("Point", "x y")
Point.__add__ = lambda self, other: Point(self.x + other.x, self.y + other.y)

MAP_SIZE = 50
DELTAS = {
    Direction.NORTH: Point(0, -1),
    Direction.EAST: Point(1, 0),
    Direction.SOUTH: Point(0, 1),
    Direction.WEST: Point(-1, 0)
}
OPPOSITES = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST
}

def find_new_direction(board, droid, moves):
    for direction in Direction:
        new_space = droid + DELTAS[direction]
        if board[new_space.y][new_space.x] == " ":
            return direction
    return OPPOSITES[moves[-1]] if moves else None

def day15(filename):
    computer = IntcodeComputer.fromFile(filename)
    computer.run()
    start = droid = Point(MAP_SIZE // 2, MAP_SIZE // 2)
    board = [[" " for x in range(MAP_SIZE)] for y in range(MAP_SIZE)]
    board[droid.y][droid.x] = "."
    direction = Direction.NORTH

    # Stack (for backtracking)
    moves = []
    found_oxygen = False

    # Go until we've explored the entire maze
    while not found_oxygen or moves:
        computer.send(direction)
        computer.run()
        output = next(computer)

        if output == Output.OXYGEN or output == Output.MOVED:
            droid += DELTAS[direction]
            board[droid.y][droid.x] = "."

            if len(moves) > 0 and direction == OPPOSITES[moves[-1]]:
                moves.pop()
            else:
                moves.append(direction)

            if output == Output.OXYGEN:
                oxygen = droid
                found_oxygen = True

            direction = find_new_direction(board, droid, moves)
        elif output == Output.WALL:
            wall = droid + DELTAS[direction]
            board[wall.y][wall.x] = "#"
            direction = find_new_direction(board, droid, moves)
        else:
            assert False, "Unrecognized response"

        assert droid.x >= 0 and droid.y >= 0

    # Now run a BFS to find the shortest distance to oxygen
    queue = []
    queue.append((start, 0))
    visited = set()
    while True:
        (node, distance) = queue.pop(0)
        visited.add(node)
        if node == oxygen:
            print(f"Moves to oxygen: {distance}")
            break

        for direction in Direction:
            new_node = node + DELTAS[direction]
            if board[new_node.y][new_node.x] == "." and new_node not in visited:
                queue.append((new_node, distance + 1))

    # Now run a BFS from OXYGEN to fill the maze
    queue = []
    queue.append((oxygen, 0))
    visited = set()
    while queue:
        (node, distance) = queue.pop(0)
        visited.add(node)

        for direction in Direction:
            new_node = node + DELTAS[direction]
            if board[new_node.y][new_node.x] == "." and new_node not in visited:
                queue.append((new_node, distance + 1))

        if not queue:
            print(f"Minutes to fill with oxygen: {distance}")



if __name__ == "__main__":
    day15(sys.argv[1])
