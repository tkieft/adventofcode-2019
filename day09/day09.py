import sys

MEMORY = 10000

def run(original_program):
    pc = 0
    relative_base = 0
    input = None
    output = None

    # Copy the program into memory
    program = [0 for i in range(MEMORY)]
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
            program[parameter_address(1)] = input
            pc += 2
        elif opcode == 4:
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

def day09(filename):
    with open(filename) as f:
        program = [int(token) for token in f.read().rstrip().split(",")]

    boost_test = run(program)
    next(boost_test)
    print(boost_test.send(1))

    boost = run(program)
    next(boost)
    print(boost.send(2))

if __name__ == "__main__":
    day09(sys.argv[1])
