import functools
import itertools
import sys

powers_of_two = [2 ** i for i in range(25)]

BUG = "#"
EMPTY = "."

def make_board(center = None):
    board = [[EMPTY for x in range(5)] for y in range(5)]
    if center: board[2][2] = center
    return board

def make_boards(count):
    boards = [make_board()]
    for _ in range(count - 1):
        add_upper_level(boards)
    return boards

def add_upper_level(boards):
    boards.insert(0, make_board(boards[0]))

def add_lower_level(boards):
    new_board = make_board()
    boards[-1][2][2] = new_board
    boards.append(new_board)

def print_board(board):
    for row in board:
        print("".join(row))
    print()

@functools.lru_cache(100)
def surrounding_points(x, y, clamp):
    points = []
    if not clamp or x > 0: points.append((x - 1, y))
    if not clamp or x < 4: points.append((x + 1, y))
    if not clamp or y > 0: points.append((x, y - 1))
    if not clamp or y < 4: points.append((x, y + 1))
    return points

def populate_square(new_board, x, y, val, num_surrounding_bugs):
    if is_bug(val):
        new_board[y][x] = EMPTY if num_surrounding_bugs != 1 else BUG
    else:
        new_board[y][x] = BUG if num_surrounding_bugs in (1, 2) else EMPTY

def biodiversity(board):
    return sum(powers_of_two[i] for i, val in enumerate(itertools.chain.from_iterable(board)) if is_bug(val))

def part1_surrounding(board, x, y):
    return sum(count_is_bug(board[yy][xx]) for (xx, yy) in surrounding_points(x, y, True))

def run_part1(board):
    new_board = make_board()
    for y, row in enumerate(board):
        for x, val in enumerate(row):
            populate_square(new_board, x, y, val, part1_surrounding(board, x, y))

    return new_board

def part1(board):
    seen = set()
    while True:
        board = run_part1(board)
        bd = biodiversity(board)
        if bd in seen:
            return bd
        seen.add(bd)

def is_bug(c):
    return c == BUG

def count_is_bug(c):
    return 1 if is_bug(c) else 0

def part2_surrounding(board, upper_board, x, y):
    surrounding = 0
    for (xx, yy) in surrounding_points(x, y, False):
        # Recurse up
        if   xx < 0:  surrounding += 1 if upper_board and is_bug(upper_board[2][1]) else 0
        elif xx == 5: surrounding += 1 if upper_board and is_bug(upper_board[2][3]) else 0
        elif yy < 0:  surrounding += 1 if upper_board and is_bug(upper_board[1][2]) else 0
        elif yy == 5: surrounding += 1 if upper_board and is_bug(upper_board[3][2]) else 0
        else:
            val = board[yy][xx]
            if isinstance(val, list):
                # Recurse down
                if yy != y: surrounding += sum(count_is_bug(c) for c in val[4 if yy < y else 0])
                else:       surrounding += sum(count_is_bug(row[4 if xx < x else 0]) for row in val)
            else:
                # Normal square
                surrounding += count_is_bug(val)

    return surrounding

def run_part2(boards):
    new_boards = make_boards(len(boards))

    for i, board in enumerate(boards):
        upper_board = boards[i - 1] if i > 0 else None
        for y, row in enumerate(board):
            for x, val in enumerate(row):
                if isinstance(val, list): continue
                populate_square(new_boards[i], x, y, val, part2_surrounding(board, upper_board, x, y))
    return new_boards

def count_bugs(board):
    return sum(count_is_bug(x) for x in itertools.chain.from_iterable(board))

def part2(boards):
    for _ in range(200):
        boards = run_part2(boards)
    return sum(count_bugs(board) for board in boards)

def day24(filename):
    with open(filename) as f:
        board = [list(line.rstrip()) for line in f if line]

    print(part1(board))

    # This runs fast enough that we can do this the stupid way. Rather than
    # creating new boards on demand, we create enough (200) at the start.
    part2_boards = [board]
    for _ in range(100):
        add_upper_level(part2_boards)
        add_lower_level(part2_boards)
    print(part2(part2_boards))

if __name__ == "__main__":
    day24(sys.argv[1])
