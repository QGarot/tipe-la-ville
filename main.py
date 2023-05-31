from database.database import Database
from build_network.map import Map
from pathfinder.road_network import RoadNetwork, Node, Point
from matplotlib import pyplot as plt
from route_manager import RouteRequest


db = Database("localhost", "root", "", "tipe_ville")
city = Map("build_network/img/map3.png", db)
# Permet de définir les stations (les noeuds)
# city.display_interactive_map()
city.display_map_with_stations()

# Permet de définir les liens entre les stations, ie lesquelles sont reliées entre elles ?
city.set_adjacency_matrix([
    [0, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0]
])

city.display_graph()
network = RoadNetwork(city.get_stations(), city.get_adjacency_matrix())


#  network.compare(1, 6, [Point.get_manhattan_distance, Point.get_euclidian_distance, Point.heuristic_null], ["#34ace0", "#33d9b2", "#ffb142"])

request = RouteRequest((413, 454), (604, 744))
print(request.get_route_data_str(network))
# print(network.path_weight([network.get_node_by_id(2), network.get_node_by_id(3), network.get_node_by_id(4), network.get_node_by_id(7)]))
