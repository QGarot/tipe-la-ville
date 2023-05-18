from database.database import Database
from build_network.map import Map


db = Database("localhost", "root", "", "tipe_ville")
city = Map("build_network/img/map2.png", db)
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
