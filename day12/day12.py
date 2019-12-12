from collections import namedtuple
import copy
import itertools
import numpy
import pprint
import re
from recordclass import recordclass, RecordClass
import sys
from typing import List, Tuple

class Point3(RecordClass):
    x: int
    y: int
    z: int

class Moon(RecordClass):
    pos: Point3
    vel: Point3

PATTERN = re.compile(r"(-?\d+)")

def cmp(x, y):
    return (x > y) - (x < y)

def applyGravity(moon: Moon, other: Moon):
    for field in moon.pos.__fields__:
        delta = cmp(moon.pos[field], other.pos[field])
        moon.vel[field] -= delta
        other.vel[field] += delta

def applyVelocity(moon: Moon):
    for field in moon.vel.__fields__:
        moon.pos[field] += moon.vel[field]

def doStep(moons: List[Moon]):
    for (moon, other) in itertools.combinations(moons, 2):
        applyGravity(moon, other)

    for moon in moons:
        applyVelocity(moon)

def moonEnergy(moon: Moon) -> int:
    potentialEnergy = sum(abs(moon.pos[field]) for field in moon.pos.__fields__)
    kineticEnergy = sum(abs(moon.vel[field]) for field in moon.vel.__fields__)
    return potentialEnergy * kineticEnergy

def systemEnergy(moons: List[Moon]) -> int:
    return sum(moonEnergy(moon) for moon in moons)

def systemState(moons: List[Moon], coord: str) -> Tuple[Tuple[int]]:
    return tuple((moon.pos[coord], moon.vel[coord]) for moon in moons)

def day12(filename):
    with open(filename) as f:
        moons = [
            Moon(Point3(*[int(match) for match in PATTERN.findall(line)]),
                 Point3(0, 0, 0))
            for line in f]

    repeat = Point3(0, 0, 0)
    states = {}
    for coord in repeat.__fields__:
        states[coord] = set()
        states[coord].add(systemState(moons, coord))

    i = 0
    while 0 in repeat or i < 1000:
        i += 1
        doStep(moons)

        for coord in repeat.__fields__:
            if repeat[coord] == 0:
                state = systemState(moons, coord)
                if state in states[coord]:
                    repeat[coord] = i
                    continue
                states[coord].add(state)

        if i == 1000:
            print(f"Total Energy after 1000 steps: {systemEnergy(moons)}")

    print(f"Repeats after {numpy.lcm(numpy.lcm(repeat.x, repeat.y), repeat.z)} steps")

if __name__ == "__main__":
    day12(sys.argv[1])
