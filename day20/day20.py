from collections import defaultdict, namedtuple
import pprint
import sys

Point = namedtuple("Point", "x y")
NodeEdge = namedtuple("NodeEdge", "node depth")
PointEdge = namedtuple("PointEdge", "point depth")

class Node:
    def __init__(self, point):
        self.point = point
        self.edges = []

    def __repr__(self):
        return f"Node({self.point.x}, {self.point.y})"

def read_maze(filename):
    with open(filename) as f:
        return [list(line[:-1]) for line in f if line]

def print_maze(maze):
    for row in maze:
        print("".join(row))
    print()

def isUppercase(val):
    return val >= "A" and val <= "Z"

def neighboring_nodes(nodes, node):
    return [nn for nn in [
        nodes.get(Point(node.point.x - 1, node.point.y)),
        nodes.get(Point(node.point.x + 1, node.point.y)),
        nodes.get(Point(node.point.x,     node.point.y - 1)),
        nodes.get(Point(node.point.x,     node.point.y + 1)),
    ] if nn]

def addPortal(portals, name, point, outward):
    portals[name].append(PointEdge(point, -1 if outward else 1))

def addHorizontalPortal(maze, portals, name, point):
    outward = point.x == 2 or point.x == len(maze[point.y]) - 3
    addPortal(portals, name, point, outward)

def addVerticalPortal(maze, portals, name, point):
    outward = point.y == 2 or point.y == len(maze) - 3
    addPortal(portals, name, point, outward)

def make_graph(maze):
    nodes = {}
    entrance = None
    exit = None

    portals = defaultdict(list)

    # First, create all the nodes
    for y, row in enumerate(maze):
        for x, val in enumerate(row):
            if val == ".":
                point = Point(x, y)
                node = nodes[point] = Node(point)
            elif isUppercase(val):
                # Horizontal letters
                if x + 1 < len(row) and isUppercase(row[x + 1]):
                    if x + 2 < len(row) and row[x + 2] == ".":
                        addHorizontalPortal(maze, portals, val + row[x + 1], Point(x + 2, y))    # Point is to right
                    else:
                        addHorizontalPortal(maze, portals, val + row[x + 1], Point(x - 1, y))    # Point is to left
                # Vertical letters
                elif y + 1 < len(maze) and x < len(maze[y + 1]) and isUppercase(maze[y + 1][x]):
                    if y + 2 < len(maze) and x < len(maze[y + 2]) and maze[y + 2][x] == ".":
                        addVerticalPortal(maze, portals, val + maze[y + 1][x], Point(x, y + 2))  # Point is below
                    else:
                        addVerticalPortal(maze, portals, val + maze[y + 1][x], Point(x, y - 1))  # Point is below

    # Now link them
    for node in nodes.values():
        for neighbor in neighboring_nodes(nodes, node):
            node.edges.append(NodeEdge(neighbor, 0))

    for portal, point_edges in portals.items():
        if portal == "AA":
            assert len(point_edges) == 1
            entrance = nodes[point_edges[0].point]
        elif portal == "ZZ":
            assert len(point_edges) == 1
            exit = nodes[point_edges[0].point]
        else:
            assert len(point_edges) == 2
            nodes[point_edges[0].point].edges.append(NodeEdge(nodes[point_edges[1].point], point_edges[0].depth))
            nodes[point_edges[1].point].edges.append(NodeEdge(nodes[point_edges[0].point], point_edges[1].depth))

    return entrance, exit

def part1(entrance, exit):
    visited = set()
    visited.add(entrance)
    queue = [(entrance, 0)]

    while queue:
        node, steps = queue.pop(0)

        if node == exit:
            return steps

        for edge in node.edges:
            if edge.node not in visited:
                visited.add(edge.node)
                queue.append((edge.node, steps + 1))

def part2(entrance, exit):
    visited = set()
    visited.add((entrance, 0))
    queue = [(entrance, 0, 0)]

    while queue:
        node, depth, steps = queue.pop(0)

        if node == exit and depth == 0:
            return steps

        for edge in node.edges:
            new_depth = depth + edge.depth
            if new_depth < 0: continue
            new_state = (edge.node, new_depth)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((*new_state, steps + 1))

def day20(filename):
    maze = read_maze(filename)
    entrance, exit = make_graph(maze)

    steps = part1(entrance, exit)
    print(steps)
    steps = part2(entrance, exit)
    print(steps)


if __name__ == "__main__":
    day20(sys.argv[1])
