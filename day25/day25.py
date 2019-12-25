import sys

from intcode import IntcodeComputer

def day25(filename):
    computer = IntcodeComputer.fromFile(filename)

    while True:
        computer.run()
        for x in computer:
            print(chr(x), end="")
        print(">", end=" ")
        try:
            for c in input():
                computer.send(ord(c))
        except EOFError:
            return
        computer.send(ord("\n"))


if __name__ == "__main__":
    day25(sys.argv[1])
