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


def compare(start_node_id: int, final_node_id: int, heuristics: list[callable], colors: list[str]) -> None:
    """
    Affiche un graphique permettant d'analyser l'efficacité de la méthode pathfinder en fonction des heuristiques
    choisies.
    :param start_node_id:
    :param final_node_id:
    :param heuristics:
    :param colors:
    """
    fig, ax = plt.subplots()
    heuristic_names = []
    loops_set = []

    for heuristic in heuristics:
        path_info = network.pathfinder(start_node_id, final_node_id, heuristic)
        loops_number = path_info[1]
        print(path_info[0])
        network.reset_nodes_properties()
        heuristic_names.append(heuristic.__name__)
        loops_set.append(loops_number)

    ax.bar(heuristic_names, loops_set, color=colors)
    ax.set_ylabel("Nombre de tours de boucle")
    ax.set_title("Efficacité du pathfinder selon l'heuristique choisie")
    plt.show()


compare(1, 6, [Point.get_manhattan_distance, Point.get_euclidian_distance, Point.heuristic_null], ["#34ace0", "#33d9b2", "#ffb142"])

request = RouteRequest(network, (596, 784), (595, 306))
print(request.get_route_data())
