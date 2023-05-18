import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from database.database import Database
from math import floor
from pathfinder.road_network import Node
import networkx as nx

# print(repr(img))
# plt.scatter(x=500, y=400, c="#FF4633", linewidths=1.3, edgecolors="#7A0C00", s=200, alpha=0.6)


class Station(Node):
    """
    Représente une station.
    Hérite de la classe Node qui représente un point d'un graphe.
    """
    def __init__(self, id, name, x, y, capacity, current_people):
        super().__init__(id, x, y)
        self.name = name
        self.capacity = capacity
        self.current_people = current_people


class Map:
    """
    Représente la carte d'une ville.
    """
    def __init__(self, city_map: str, db: Database = None):
        self.map = city_map
        self.image = np.asarray(Image.open(city_map))
        self.fig, self.ax = plt.subplots()
        self.db = db
        self.graph = None
        self.adjacency_matrix = None

    def place_station(self, event) -> None:
        """
        Sur la carte de la ville, un clique de souris permet de positionner virtuellement une station.
        Lors d'un clique, un nouvel enregistrement se fait dans la table "stations" de la base de données.
        Cet enregistrement contient notamment les coordonnées de la station.
        :param event:
        :return:
        """
        x = event.xdata
        y = event.ydata
        # print(event.xdata)
        # print(event.ydata)
        self.db.set("INSERT INTO stations (name, localisation_x, localisation_y) VALUES ('test', " + str(floor(x)) + "," + str(floor(y)) + ");")

    def display_interactive_map(self) -> None:
        """
        Affiche la carte de la ville sur laquelle il est possible de positionner des stations.
        :return:
        """
        self.fig.canvas.mpl_connect('button_press_event', self.place_station)
        plt.axis([0, 1420, 0, 829])
        plt.imshow(self.image, extent=(0, 1420, 0, 829))
        plt.show()

    def display_map_with_stations(self) -> None:
        """
        Affiche la carte de la ville ainsi que les différentes stations.
        :return:
        """
        for station in self.get_stations():
            plt.text(x=station.get_x(),
                     y=station.get_y(),
                     s=str(station.get_id()),
                     horizontalalignment="center",
                     bbox=dict(boxstyle="round", color="#FF4633", alpha=0.6))

        plt.axis([0, 1420, 0, 829])
        plt.imshow(self.image, extent=(0, 1420, 0, 829))
        plt.show()

    def get_stations(self) -> list[Station]:
        """
        :return: L'ensemble des stations de la ville.
        """
        stations = self.db.get("SELECT * FROM stations")
        for i in range(len(stations)):
            station = stations[i]
            id, name, x, y = station[0], station[1], station[2], station[3]
            stations[i] = Station(id, name, x, y, station[4], station[5])

        return stations

    def set_adjacency_matrix(self, matrix: list[list]) -> None:
        """
        Initialise la matrice d'adjacence des stations : celle-ci représente les liens entre elles.
        :param matrix:
        :return:
        """
        self.adjacency_matrix = matrix

    def get_adjacency_matrix(self) -> list[list]:
        """
        :return: La matrice d'adjacence
        """
        return self.adjacency_matrix

    def display_graph(self) -> None:
        """
        Crée et affiche le graphe représentant les stations de la ville
        :return:
        """
        self.graph = nx.Graph()

        for station in self.get_stations():
            self.graph.add_node(station.get_id(), pos=(station.get_x(), station.get_y()))

        try:
            n = len(self.get_adjacency_matrix())
            for i in range(n):
                for j in range(n):
                    if self.get_adjacency_matrix()[i][j] == 1:
                        self.graph.add_edge(i + 1, j + 1)
        except:
            print("Il faut créer la matrice d'adj. !")

        nx.draw(self.graph, nx.get_node_attributes(self.graph, 'pos'), with_labels=True)
        plt.show()
