import copy
import sys

def run(program):
    pc = 0

    while True:
        opcode = program[pc]
        if opcode == 1:
            program[program[pc + 3]] = program[program[pc + 1]] + program[program[pc + 2]]
            pc += 4
        elif opcode == 2:
            program[program[pc + 3]] = program[program[pc + 1]] * program[program[pc + 2]]
            pc += 4
        elif opcode == 99:
            break
        else:
            assert False, "Unrecognized opcode"

    return program[0]

def day02(filename):
    with open(filename) as f:
        program = [int(item) for item in f.readline().split(",")]

    # Part 2
    p = copy.copy(program)
    p[1] = 12
    p[2] = 2
    print(run(p))

    # Part 2
    noun = 0
    verb = 0
    while True:
        p = copy.copy(program)
        p[1] = noun
        p[2] = verb

        if run(p) == 19690720:
            print(100 * noun + verb)
            break

        verb += 1
        if verb == 100:
            verb = 0
            noun += 1

if __name__ == "__main__":
    day02(sys.argv[1])
