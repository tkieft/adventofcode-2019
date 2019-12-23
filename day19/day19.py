import statistics
import sys

from intcode import IntcodeComputer

def check(x, y, program):
    computer = IntcodeComputer(program)
    computer.send(x)
    computer.send(y)
    computer.run()
    return next(computer) == 1

def day19(filename):
    with open(filename) as f:
        program = [int(token) for token in f.read().rstrip().split(",")]

    in_part1_area = 0

    x = x_start = 0
    x_end = 0
    y = 0

    while True:
        x = x_start
        started = False

        while True:
            if check(x, y, program):
                if not started:
                    started = True
                    x_start = x
                    x = max(x, x_end - 1)
            elif started:
                x_end = x
                break

            x += 1

        if y < 50:
            in_part1_area += min(x_end, 50) - min(x_start, 50)

        if y == 49:
            print(in_part1_area)

        if x_end - x_start >= 100:
            x_square = x_end - 100
            found_square = False
            while check(x_square, y, program) and check(x_square, y + 99, program) \
                and check(x_square + 99, y, program) and check(x_square + 99, y + 99, program):
                x_square -= 1
                found_square = True

            if found_square:
                print((x_square + 1) * 10000 + y)
                break

        y += 1


if __name__ == "__main__":
    day19(sys.argv[1])
