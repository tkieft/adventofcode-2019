import math
import re
import sys

def parseFile(f):
    pattern = re.compile(r"(.*?) => (.*)")
    reactions = {}

    for line in f:
        match = pattern.match(line)
        inputs = [(int(compound.split()[0]), compound.split()[1]) for compound in match[1].split(", ")]
        output = tuple(match[2].split())
        reactions[output[1]] = (int(output[0]), inputs)

    return reactions

def make_fuel(items_remaining, reactions):
    ore_needed = 0
    items_needed = {"FUEL": 1}

    while len(items_needed) != 0:
        (item, num_needed) = next(iter(items_needed.items()))
        del items_needed[item]

        used = min(items_remaining.setdefault(item, 0), num_needed)
        items_remaining[item] -= used
        num_needed -= used

        if num_needed == 0:
            continue

        (num_produced, ingredients) = reactions[item]
        num_reactions = math.ceil(num_needed / num_produced)

        items_remaining[item] = num_reactions * num_produced - num_needed

        for ingredient in ingredients:
            if (ingredient[1] == "ORE"):
                ore_needed += ingredient[0] * num_reactions
            else:
                items_needed[ingredient[1]] = items_needed.get(ingredient[1], 0) + ingredient[0] * num_reactions

    return ore_needed

def day14(filename):
    with open(filename) as f:
        reactions = parseFile(f)

    items_remaining = {}
    ore_needed = make_fuel(items_remaining, reactions)
    print(ore_needed)

    fuel_made = 0

    while ore_needed <= 1000000000000:
        fuel_made += 1
        ore_needed += make_fuel(items_remaining, reactions)

    print(fuel_made)


if __name__ == "__main__":
    day14(sys.argv[1])
