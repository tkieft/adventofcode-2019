import copy
import sys

def run(program, stdin):
    pc = 0

    def parameter(index):
        return program[pc + index] \
            if program[pc] // (10 ** (index + 1)) % 10 \
            else program[program[pc + index]]

    while True:
        opcode = program[pc] % 100

        if opcode == 1:
            program[program[pc + 3]] = parameter(1) + parameter(2)
            pc += 4
        elif opcode == 2:
            program[program[pc + 3]] = parameter(1) * parameter(2)
            pc += 4
        elif opcode == 3:
            assert stdin
            program[program[pc + 1]] = stdin.pop()
            pc += 2
        elif opcode == 4:
            print(parameter(1))
            pc += 2
        elif opcode == 5:
            pc = parameter(2) if parameter(1) else pc + 3
        elif opcode == 6:
            pc = parameter(2) if not parameter(1) else pc + 3
        elif opcode == 7:
            program[program[pc + 3]] = 1 if parameter(1) < parameter(2) else 0
            pc += 4
        elif opcode == 8:
            program[program[pc + 3]] = 1 if parameter(1) == parameter(2) else 0
            pc += 4
        elif opcode == 99:
            break
        else:
            assert False, "Unrecognized opcode"

def day05(filename):
    with open(filename) as f:
        program = [int(item) for item in f.readline().split(",")]

    run(copy.copy(program), [1])
    print()
    run(copy.copy(program), [5])


if __name__ == "__main__":
    day05(sys.argv[1])
