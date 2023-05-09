from pathfinder.road_network import Node, RoadNetwork

# some tests
nodes = [
    Node(0, 0, 0),
    Node(1, 2, 2),
    Node(2, 2, -1),
    Node(3, 5, 2),
    Node(4, 5, -1),
    Node(5, 7, 1)
]

matrix = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0]
]

rn = RoadNetwork(nodes, matrix)
print(rn.pathfinder(0, 4))

