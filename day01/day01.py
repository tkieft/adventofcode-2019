import sys

def calcfuel(mass, fuel_costs_fuel = False):
    fuel = mass // 3 - 2
    return calcfuel(fuel, True) + fuel if fuel > 0 and fuel_costs_fuel else max(fuel, 0)

def day01(filename):
    with open(filename) as f:
        masses = [int(line) for line in f]

    # Part 1
    fuel = sum(map(calcfuel, masses))
    print(fuel)

    # Part 2
    fuel = sum([calcfuel(mass, True) for mass in masses])
    print(fuel)

if __name__ == "__main__":
    day01(sys.argv[1])
