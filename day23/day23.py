import sys

from intcode import IntcodeComputer

NUM_COMPUTERS = 50

def day23(filename):
    computers = [IntcodeComputer.fromFile(filename) for _ in range(NUM_COMPUTERS)]
    for i, computer in enumerate(computers):
        computer.send(i)
        computer.run()

    queues = [[] for i in range(NUM_COMPUTERS)]

    nat = None
    released_y = None

    while True:
        for queue, computer in zip(queues, computers):
            if len(queue) == 0:
                computer.send(-1)
            else:
                for message in queue:
                    computer.send(message[0])
                    computer.send(message[1])
                queue.clear()
            computer.run()
            output = list(computer)
            for i in range(0, len(output), 3):
                recipient, x, y = output[i], output[i + 1], output[i + 2]

                if recipient == 255:
                    if nat is None:
                        # Part 1
                        print(y)
                    nat = (x, y)
                else:
                    queues[recipient].append((x, y))

        if not any(queues):
            if nat[1] == released_y:
                # Part 2
                print(released_y)
                return

            released_y = nat[1]
            computers[0].send(nat[0])
            computers[0].send(nat[1])
            computers[0].run()


if __name__ == "__main__":
    day23(sys.argv[1])
