import sys

MEMORY_SIZE = 10000
BOARD_SIZE = 200

def run(original_program):
    pc = 0
    relative_base = 0
    input = None
    output = None

    # Copy the program into memory
    program = [0 for i in range(MEMORY_SIZE)]
    for i, arg in enumerate(original_program):
        program[i] = arg

    def parameter_address(index):
        mode = program[pc] // (10 ** (index + 1)) % 10
        if mode == 0:  # position
            return program[pc + index]
        elif mode == 1:  # immediate
            return pc + index
        elif mode == 2:  # relative
            return relative_base + program[pc + index]
        else:
            assert False, "Unrecognized parameter mode"

    def parameter(index):
        return program[parameter_address(index)]

    while True:
        opcode = program[pc] % 100

        if opcode == 1:
            program[parameter_address(3)] = parameter(1) + parameter(2)
            pc += 4
        elif opcode == 2:
            program[parameter_address(3)] = parameter(1) * parameter(2)
            pc += 4
        elif opcode == 3:
            input = yield output
            output = None
            program[parameter_address(1)] = input
            pc += 2
        elif opcode == 4:
            if output is not None:
                temp = yield output
                assert temp is None
            output = parameter(1)
            pc += 2
        elif opcode == 5:
            pc = parameter(2) if parameter(1) else pc + 3
        elif opcode == 6:
            pc = parameter(2) if not parameter(1) else pc + 3
        elif opcode == 7:
            program[parameter_address(3)] = 1 if parameter(1) < parameter(2) else 0
            pc += 4
        elif opcode == 8:
            program[parameter_address(3)] = 1 if parameter(1) == parameter(2) else 0
            pc += 4
        elif opcode == 9:  # relative base offset
            relative_base += parameter(1)
            pc += 2
        elif opcode == 99:
            yield output
            return
        else:
            assert False, "Unrecognized opcode"

def paint_hull(program, start_color = 0):
    board = [[None for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
    robot = (BOARD_SIZE // 2, BOARD_SIZE // 2)
    facing = 1

    board[robot[1]][robot[0]] = start_color

    moves = [
        (1, 0),
        (0, -1),
        (-1, 0),
        (0, 1)
    ]

    computer = run(program)
    assert next(computer) is None

    while True:
        try:
            board[robot[1]][robot[0]] = computer.send(board[robot[1]][robot[0]] or 0)
            turn = next(computer)
            facing = (facing + (-1 if turn else 1)) % 4
            move = moves[facing]
            robot = (robot[0] + move[0], robot[1] + move[1])
            assert robot[0] >= 0 and robot[1] >= 0
        except StopIteration:
            break

    return board

def day11(filename):
    with open(filename) as f:
        program = [int(token) for token in f.read().rstrip().split(",")]

    board = paint_hull(program)
    print(sum(row.count(0) + row.count(1) for row in board))
    print()

    board = paint_hull(program, 1)
    first1 = min(row.index(1) for row in board if 1 in row)
    for row in board:
        if row.count(1):
            print("".join(['#' if i == 1 else ' ' for i in row ]).rstrip()[first1:])


if __name__ == "__main__":
    day11(sys.argv[1])
