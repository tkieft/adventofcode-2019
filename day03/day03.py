import sys

ORIGIN = (0, 0)

def plotwire(wire):
    point = ORIGIN
    points = {}
    steps = 0
    for move in wire:
        magnitude = int(move[1:])
        delta = {
            "U": (0, -1),
            "D": (0, 1),
            "L": (-1, 0),
            "R": (1, 0)}[move[0]]

        for _ in range(magnitude):
            steps += 1
            point = (point[0] + delta[0], point[1] + delta[1])
            if point not in points:
                points[point] = steps

    return points

def distance(point, other):
    return abs(point[0] - other[0]) + abs(point[1] - other[1])

def day03(filename):
    with open(filename) as f:
        wire1 = f.readline().rstrip().split(",")
        wire2 = f.readline().rstrip().split(",")

    points1 = plotwire(wire1)
    points2 = plotwire(wire2)

    print(min(distance(point, ORIGIN) for point in points1 if point in points2))
    print(min(points1[point] + points2[point] for point in points1 if point in points2))


if __name__ == "__main__":
    day03(sys.argv[1])
