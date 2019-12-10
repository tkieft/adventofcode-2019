import math
import sys

def angle(other):
    atan = -math.atan2(other[1], other[0])
    atan += math.pi / 2
    return atan + math.pi * 2 if atan < 0 else atan

def distance(point):
    return abs(point[0]) + abs(point[1])

def relative_position(base, other):
    return (other[0] - base[0], base[1] - other[1])  # y is positive going up

def in_line_of_sight(point, further_point):
    if point[0] == 0 and further_point[0] == 0:
        return further_point[1] / point[1] == abs(further_point[1]) / abs(point[1])
    if point[1] == 0 and further_point[1] == 0:
        return further_point[0] / point[0] == abs(further_point[0]) / abs(point[0])

    if 0 in point: return False

    multiplier = (further_point[0] / point[0], further_point[1] / point[1])
    abs_multiplier = (abs(further_point[0]) / abs(point[0]), abs(further_point[1]) / abs(point[1]))
    return multiplier[0] == multiplier[1] == abs_multiplier[0] == abs_multiplier[1]

def part1(board):
    most = (None, 0)
    asteroids = [(x, y) for y,row in enumerate(board) for x,loc in enumerate(row) if loc == '#']

    for asteroid in asteroids:
        # Must go from inward to outward
        relative_asteroids = sorted([relative_position(asteroid, other) for other in asteroids],
                                    key = distance)
        seen_asteroids = []

        for other in relative_asteroids:
            if other == (0, 0):
                continue
            for seen in seen_asteroids:
                if in_line_of_sight(seen, other):
                    break
            else:
                seen_asteroids.append(other)

        if len(seen_asteroids) > most[1]:
            most = (asteroid, len(seen_asteroids))

    return most

def part2(board, laser):
    asteroids = [(x, y) for y,row in enumerate(board) for x,loc in enumerate(row) if loc == '#' and (x,y) != laser]
    relative_asteroids = [relative_position(laser, asteroid) for asteroid in asteroids]
    asteroid_angles = [angle(other) for other in relative_asteroids]
    asteroids = list(zip(asteroids, relative_asteroids, asteroid_angles))

    # Sorted by angle, then distance
    asteroids.sort(key = lambda asteroid: distance(asteroid[1]))
    asteroids.sort(key = lambda asteroid: asteroid[2])

    asteroids_vaporized = 0

    i = 0
    current_angle = -1
    while asteroids:
        if asteroids[i][2] > current_angle:
            current_angle = asteroids[i][2] + 1e-9  # sweep ahead just a little bit
            asteroids_vaporized += 1

            if asteroids_vaporized == 200:
                return asteroids[i][0]

            asteroids.remove(asteroids[i])
        else:
            i += 1

        if i == len(asteroids):
            i = 0
            current_angle = -1e-9  # Reset the sweep

def day10(filename):
    with open(filename) as f:
        board = [list(line.rstrip()) for line in f]

    location, seen = part1(board)
    print(f"Monitoring station should be located at {location} [{seen} asteroids seen]")
    print(f"200th asteroid vaporized is located at {part2(board, location)}")

if __name__ == "__main__":
    day10(sys.argv[1])
