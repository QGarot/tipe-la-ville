from database.database import Database
from build_network.map import Map
from pathfinder.road_network import RoadNetwork, Node
from matplotlib import pyplot as plt


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
    [0, 0, 0, 1, 0, 1, 1, 0],
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
        loops_number = network.pathfinder(start_node_id, final_node_id, heuristic)[1]
        network.reset_nodes_properties()
        heuristic_names.append(heuristic.__name__)
        loops_set.append(loops_number)

    ax.bar(heuristic_names, loops_set, color=colors)
    ax.set_ylabel("Nombre de tours de boucle")
    ax.set_title("Efficacité du pathfinder selon l'heuristique choisie")
    plt.show()


compare(1, 5, [Node.get_manhattan_distance, Node.get_distance, Node.heuristic_null], ["blue", "green", "orange"])
