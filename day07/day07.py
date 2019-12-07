import copy
import itertools
import sys

def run(program):
    pc = 0
    input = None
    output = None

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
            input = yield output
            program[program[pc + 1]] = input
            pc += 2
        elif opcode == 4:
            output = parameter(1)
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
            yield output
            return
        else:
            assert False, "Unrecognized opcode"

def run_amplifiers(ordering, program):
    amplifiers = [run(copy.copy(program)) for phase in ordering]

    for i, phase in enumerate(ordering):
        next(amplifiers[i])
        amplifiers[i].send(phase)

    index = 0
    value = 0
    while True:
        try:
            value = amplifiers[index].send(value)
            index = (index + 1) % len(amplifiers)
        except StopIteration:
            return value

def day07(filename):
    with open(filename) as f:
        program = [int(token) for token in f.read().rstrip().split(",")]

    print(max(run_amplifiers(ordering, program) for ordering in itertools.permutations(range(5))))
    print(max(run_amplifiers(ordering, program) for ordering in itertools.permutations(range(5, 10))))


if __name__ == "__main__":
    day07(sys.argv[1])
