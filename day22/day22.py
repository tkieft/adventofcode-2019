import sys

NUM_CARDS_PART_1 = 10007
NUM_CARDS_PART_2 = 119315717514047
NUM_ITERATIONS_PART_2 = 101741582076661

def parse(filename):
    with open(filename) as f:
        instructions = [line.rstrip() for line in f]

    parsed_instructions = []
    for line in instructions:
        if line.startswith("deal into new stack"): parsed_instructions.append(["REVERSE"])
        elif line.startswith("cut"): parsed_instructions.append(["SHIFT", int(line.split()[1])])
        elif line.startswith("deal with increment"): parsed_instructions.append(["MULTIPLY", int(line.split()[3])])
    return parsed_instructions

def reverse(instructions, num_cards):
    instructions = list(reversed(instructions))
    for instruction in instructions:
        if instruction[0] == "SHIFT":
            instruction[1] = -instruction[1]
        elif instruction[0] == "MULTIPLY":
            instruction[0] = "INVERSE"
    return instructions

def compress(instructions, mod):
    # compress instructions into ax + b
    a = 1
    b = 0

    for instruction in instructions:
        if instruction[0] == "REVERSE":
            b = mod - b - 1
        elif instruction[0] == "SHIFT":
            b = b - instruction[1]
        elif instruction[0] == "INVERSE":
            inverse = pow(instruction[1], mod - 2, mod)
            b *= inverse
            a *= inverse

        a %= mod
        b %= mod

    return a, b

def do_shuffle(instructions, num_cards, card):
    for instruction in instructions:
        if instruction[0] == "REVERSE":
            card = num_cards - card - 1
        elif instruction[0] == "SHIFT":
            card = (card - instruction[1]) % num_cards
        elif instruction[0] == "MULTIPLY":
            card = card * instruction[1] % num_cards
        elif instruction[0] == "INVERSE":
            card = card * pow(instruction[1], num_cards - 2, num_cards) % num_cards
    return card

def recursive_linear(a, b, mod, num_iterations):
    # a(ax + b) + b = a^2x + ab + b
    if num_iterations == 1:
        return a, b
    elif num_iterations % 2 == 0:
        return recursive_linear(a ** 2 % mod, (a * b + b) % mod, mod, num_iterations // 2)
    else:
        c,d = recursive_linear(a, b, mod, num_iterations - 1)
        return (a * c) % mod,(a * d + b) % mod

def day22(filename):
    instructions = parse(filename)

    card = do_shuffle(instructions, NUM_CARDS_PART_1, 2019)
    print(card)

    instructions = reverse(instructions, NUM_CARDS_PART_2)
    a, b = compress(instructions, NUM_CARDS_PART_2)
    a, b = recursive_linear(a, b, NUM_CARDS_PART_2, NUM_ITERATIONS_PART_2)

    print((a * 2020 + b) % NUM_CARDS_PART_2)

if __name__ == "__main__":
    day22(sys.argv[1])
