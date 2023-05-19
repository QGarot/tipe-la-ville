from pathfinder.road_network import Node, RoadNetwork

# some tests
nodes = [
    Node(1, 0, 0),
    Node(2, 2, 2),
    Node(3, 2, -1),
    Node(4, 5, 2),
    Node(5, 5, -1),
    Node(6, 7, 1)
]

matrix = [
    [0, 1, 1, 0, 0, 0],
    [1, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0]
]

import time

res = 0
def ftest():
    t0 = time.perf_counter_ns()
    for i in range(10):
        print(i)
    t1 = time.perf_counter_ns()
    return t1 - t0


print(ftest())
