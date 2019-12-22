from collections import namedtuple
import itertools
from priorityqueue import PriorityQueue
import queue
import sys

Point = namedtuple("Point", "x y")

class Node:
    def __init__(self, point, val):
        self.point = point
        self.val = val
        self.neighbors = None

    def __repr__(self):
        return f"Node({self.point.x}, {self.point.y})"


def neighboring_nodes(nodes, node):
    return [nn for nn in [
        nodes.get(Point(node.point.x - 1, node.point.y)),
        nodes.get(Point(node.point.x + 1, node.point.y)),
        nodes.get(Point(node.point.x,     node.point.y - 1)),
        nodes.get(Point(node.point.x,     node.point.y + 1)),
    ] if nn]

def read_maze(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f]

def run_bfs(start, dest_nodes):
    queue = [(start, frozenset(), 0)]
    visited = set()

    distances = {}

    while queue and len(distances) != len(dest_nodes) - 1:
        node, doors, distance = queue.pop(0)
        visited.add(node)

        if node != start and node in dest_nodes and node not in distances:
            distances[node.val] = (distance, node, doors)
        elif node.val >= "A" and node.val <= "Z":
            doors = doors.union(node.val.lower())

        for neighbor in node.neighbors:
            if neighbor in visited:
                continue
            queue.append((neighbor, doors, distance + 1))

    return distances

def make_graph(maze):
    num_keys = 0
    nodes = {}
    entrances = []

    # First, create all the nodes
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            if val == "#":
                continue

            point = Point(x, y)
            node = nodes[point] = Node(point, val)
            if val == "@":
                entrances.append(node)
            elif val >= "a" and val <= "z":
                num_keys += 1

    # Now link them
    for node in nodes.values():
        node.neighbors = neighboring_nodes(nodes, node)

    # Run a BFS to find the shortest path between each pair of nodes, keeping track of which doors are along the way
    dest_nodes = set(node for node in nodes.values() if node.val >= "a" and node.val <= "z")
    start_nodes = dest_nodes.union(entrances)
    distances = {}
    for node in start_nodes:
        distances[node] = run_bfs(node, dest_nodes)

    return nodes, distances, entrances,num_keys

def find_steps(nodes, distances, entrances, num_keys):
    visited = set()
    queue = PriorityQueue()
    queue.add_task((frozenset(entrances), frozenset()), 0)

    while True:
        steps, (nodes, keys) = queue.pop_task()
        visited.add((nodes, keys))

        if len(keys) == num_keys:
            print (f"Steps: {steps}")
            print (f"Visited {len(visited)} nodes")
            break

        for node in nodes:
            new_nodes = nodes - {node}
            reachable_keys = filter(
                lambda key: not distances[node][key][2] - keys,
                distances[node].keys() - keys
            )

            for key in reachable_keys:
                distance, new_node, _ = distances[node][key]
                queue.add_task((new_nodes.union((new_node,)), keys.union(key)), steps + distance)


def part1(filename):
    maze = read_maze(filename)
    nodes, distances, entrances, num_keys = make_graph(maze)
    find_steps(nodes, distances, entrances, num_keys)

def part2(filename):
    maze = read_maze(filename)

    # Modify the maze
    ctr = len(maze) // 2
    maze[ctr][ctr] = "#"
    maze[ctr][ctr + 1] = "#"
    maze[ctr][ctr - 1] = "#"
    maze[ctr + 1][ctr] = "#"
    maze[ctr - 1][ctr] = "#"
    maze[ctr + 1][ctr + 1] = "@"
    maze[ctr + 1][ctr - 1] = "@"
    maze[ctr - 1][ctr + 1] = "@"
    maze[ctr - 1][ctr - 1] = "@"

    nodes, distances, entrances, num_keys = make_graph(maze)
    find_steps(nodes, distances, entrances, num_keys)

def day18(filename):
    part1(filename)
    part2(filename)

if __name__ == "__main__":
    day18(sys.argv[1])
