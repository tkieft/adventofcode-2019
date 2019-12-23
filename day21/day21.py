from intcode import IntcodeComputer
import sys

part_1_program = """NOT C J
NOT A T
OR T J
AND D J
NOT B T
AND C T
OR T J
WALK
"""

part_2_program = """NOT C J
AND H J
NOT A T
OR T J
AND D J
NOT B T
AND D T
OR T J
RUN
"""

def run_program(computer, program):

    for c in program:
        computer.send(ord(c))

    computer.run()

    for x in computer:
        if x < 256:
            print(chr(x), end="")
        else:
            print(x)


def day21(filename):
    computer = IntcodeComputer.fromFile(filename)
    run_program(computer, part_1_program)
    print()

    computer = IntcodeComputer.fromFile(filename)
    run_program(computer, part_2_program)


if __name__ == "__main__":
    day21(sys.argv[1])
