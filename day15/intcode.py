import copy

MEMORY_SIZE = 10000

class InputRequired(RuntimeError):
    pass

class IntcodeComputer:
    @classmethod
    def fromFile(cls, filename):
        with open(filename) as f:
            program = [int(token) for token in f.read().rstrip().split(",")]
        return cls(program)

    def __init__(self, program):
        self._pc = 0
        self._relative_base = 0
        self._input = []
        self._output = []
        self.finished = False

        # Copy the program into memory
        self._memory = copy.copy(program)
        self._memory.extend([0] * (MEMORY_SIZE - len(program)))

    def _parameter_address(self, index):
        mode = self._memory[self._pc] // (10 ** (index + 1)) % 10
        if mode == 0:  # position
            return self._memory[self._pc + index]
        elif mode == 1:  # immediate
            return self._pc + index
        elif mode == 2:  # relative
            return self._relative_base + self._memory[self._pc + index]
        else:
            assert False, "Unrecognized parameter mode"

    def _parameter(self, index):
        return self._memory[self._parameter_address(index)]

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._output) == 0: raise StopIteration()
        return self._output.pop(0)

    def run(self):
        while True:
            opcode = self._memory[self._pc] % 100

            if opcode == 1:
                self._memory[self._parameter_address(3)] = self._parameter(1) + self._parameter(2)
                self._pc += 4
            elif opcode == 2:
                self._memory[self._parameter_address(3)] = self._parameter(1) * self._parameter(2)
                self._pc += 4
            elif opcode == 3:
                if len(self._input) == 0: return
                self._memory[self._parameter_address(1)] = self._input.pop(0)
                self._pc += 2
            elif opcode == 4:
                self._output.append(self._parameter(1))
                self._pc += 2
            elif opcode == 5:
                self._pc = self._parameter(2) if self._parameter(1) else self._pc + 3
            elif opcode == 6:
                self._pc = self._parameter(2) if not self._parameter(1) else self._pc + 3
            elif opcode == 7:
                self._memory[self._parameter_address(3)] = 1 if self._parameter(1) < self._parameter(2) else 0
                self._pc += 4
            elif opcode == 8:
                self._memory[self._parameter_address(3)] = 1 if self._parameter(1) == self._parameter(2) else 0
                self._pc += 4
            elif opcode == 9:  # relative base offset
                self._relative_base += self._parameter(1)
                self._pc += 2
            elif opcode == 99:
                self.finished = True
                return
            else:
                assert False, "Unrecognized opcode"

    def send(self, input):
        self._input.append(input)
