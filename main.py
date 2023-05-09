import networkx as nx
from database.database import Database
import matplotlib.pyplot as plt
from platforms import Platform
from stations import Station


adjacency_matrix = [
    [0, 1, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0]
]
stations_collection = []
platforms_collection = []

# Base de données
db = Database("localhost", "root", "", "tipe_ville")
stations = db.select("*", "stations")
Platform.generate_with_adjacency_matrix(db, adjacency_matrix)
platforms = db.select("*", "platforms")

# Création des objets représentant les enregistrements de la BDD
for station in stations:
    id, name, x, y = station[0], station[1], station[2], station[3]
    stations_collection.append(Station(id, name, x, y, station[4], station[5]))

for platform in platforms:
    id, station_id, current_people, target_platform_id, is_open = platform[0], platform[1], platform[2], platform[3],\
                                                                  platform[4]
    platforms_collection.append(Platform(id, station_id, target_platform_id, current_people, is_open))

# Graphes
G = nx.Graph()
#   1. Noeuds
for station in stations_collection:
    G.add_node(station.id, pos=(station.x, station.y))

#   2. Arêtes
for platform in platforms_collection:
    u = platform.station_id
    v = platforms_collection[platform.target_platform_id - 1].station_id
    G.add_edge(u, v)


nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=True)
plt.show()
