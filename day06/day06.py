import sys

class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.children = []

def _orbitCount(node, depth):
    return depth + sum(_orbitCount(child, depth + 1) for child in node.children)

def orbitCount(node):
    return sum(_orbitCount(child, 1) for child in node.children)

def pathToRoot(node):
    parents = {}
    depth = 0
    while node.parent != None:
        node = node.parent
        depth += 1
        parents[node] = depth
    return parents

def orbitalTransfer(nodes):
    youpath = pathToRoot(nodes["YOU"])
    santapath = pathToRoot(nodes["SAN"])

    overlap_nodes = [key for key in youpath if key in santapath]
    closest_common_ancestor = min(overlap_nodes, key=lambda x: youpath[x])
    return youpath[closest_common_ancestor] + santapath[closest_common_ancestor] - 2

def day06(filename):
    nodes = {}

    with open(filename) as f:
        for line in f:
            orbitee, orbiter = line.rstrip().split(")")
            orbitee = nodes.setdefault(orbitee, Node(orbitee))
            orbiter = nodes.setdefault(orbiter, Node(orbiter))
            orbiter.parent = orbitee
            orbitee.children.append(orbiter)

    print(orbitCount(nodes["COM"]))
    print(orbitalTransfer(nodes))

if __name__ == "__main__":
    sys.setrecursionlimit(2000)  # LOL python
    day06(sys.argv[1])
