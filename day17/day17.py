from collections import namedtuple
from intcode import *
import sys

Point = namedtuple("Point", "x y")
Point.__add__ = lambda point, other: Point(point.x + other.x, point.y + other.y)

NORTH = Point(0, -1)
SOUTH = Point(0, 1)
EAST = Point(1, 0)
WEST = Point(-1, 0)

def day17(filename):
    with open(filename) as f:
        program = [int(token) for token in f.read().rstrip().split(",")]

    ## PART 1: Find Alignment Parameter Sum

    program[0] = 2
    computer = IntcodeComputer(program)
    computer.run()

    board = []
    row = []
    for output in computer:
        char = chr(output)
        if char == "\n":
            if not row: break
            board.append(row)
            row = []
        else:
            row.append(char)

    alignment_parameter_sum = 0

    robot_start = None

    for y, row in enumerate(board):
        for x, value in enumerate(row):
            if value == "^": robot_start = Point(x, y)
            if y == 0 or x == 0 or y == len(board) - 1 or x == len(row) - 1: continue
            if value != "#": continue
            if board[y][x - 1] != "#" or board[y][x + 1] != "#": continue
            if board[y - 1][x] != "#" or board[y + 1][x] != "#": continue
            alignment_parameter_sum += y * x

    print(f"Sum of alignment parameters: {alignment_parameter_sum}")

    ## PART 2: Move robot

    # First find the pathway
    moves = []
    position = robot_start
    direction = NORTH
    while True:
        new_direction = None
        if direction.x == 0:  # Facing north or south, check east / west
            if position.x != 0 and board[position.y][position.x - 1] == "#":
                new_direction = WEST
            elif position.x != len(board[position.y]) - 1 and board[position.y][position.x + 1] == "#":
                new_direction = EAST
        else:  # Facing east or west, check north / south
            if position.y != 0 and board[position.y - 1][position.x] == "#":
                new_direction = NORTH
            elif position.y != len(board) - 1 and board[position.y + 1][position.x] == "#":
                new_direction = SOUTH

        if not new_direction:
            break

        distance = 0
        while True:
            new_position = position + new_direction

            if new_position.x == -1 or new_position.y == -1: break
            if new_position.y == len(board) or new_position.x == len(board[new_position.y]): break
            if board[new_position.y][new_position.x] == ".": break

            distance += 1
            position = new_position

        move = None
        if new_direction == EAST: move = ("R", distance) if direction == NORTH else ("L", distance) if direction == SOUTH else None
        if new_direction == WEST: move = ("L", distance) if direction == NORTH else ("R", distance) if direction == SOUTH else None
        if new_direction == NORTH: move = ("R", distance) if direction == WEST else ("L", distance) if direction == EAST else None
        if new_direction == SOUTH: move = ("L", distance) if direction == WEST else ("R", distance) if direction == EAST else None
        assert move
        moves.append(move)

        direction = new_direction

    print()
    print(f"{len(moves)} moves")
    print(', '.join(move[0] + str(move[1]) for move in moves))
    print()

    # Create and run program (by hand)
    main = ["A", "A", "B", "C", "B", "A", "C", "B", "C", "A"]
    a = [("L", 6), ("R", 12), ("L", 6), ("L", 8), ("L", 8)]
    b = [("L", 6), ("R", 12), ("R", 8), ("L", 8)]
    c = [("L", 4), ("L", 4), ("L", 6)]

    for output in computer:
        print(chr(output), end="")

    for i, x in enumerate(main):
        computer.send(ord(x))
        if i != len(main) - 1:
            computer.send(ord(","))
    computer.send(ord("\n"))

    for output in computer:
        print(chr(output), end="")

    for routine in (a, b, c):
        for i, dir in enumerate(routine):
            computer.send(ord(dir[0]))
            computer.send(ord(","))
            for char in str(dir[1]):
                computer.send(ord(char))
            if i != len(routine) - 1:
                computer.send(ord(","))
        computer.send(ord("\n"))

        for output in computer:
            print(chr(output), end="")

    computer.send(ord("n")) # continuous video feed
    computer.send(ord("\n"))

    computer.run()

    for output in computer:
        if output < 128:
            print(chr(output), end="")
        else:
            print(f"Dust collected: {output}")


if __name__ == "__main__":
    day17(sys.argv[1])
