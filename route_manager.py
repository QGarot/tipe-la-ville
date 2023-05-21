from pathfinder.road_network import RoadNetwork, Point
from math import ceil
from build_network.map import Station, Map
from database.database import Database


class Queue:
    """
    Classe implémentant la structure de file d'attente.
    """
    def __init__(self):
        self.content = []

    def is_empty(self):
        return len(self.content) == 0

    def push(self, x):
        self.content.append(x)

    def pull(self):
        return self.content.pop(0)

    def front(self):
        return self.content[0]


class RouteRequest:
    """
    Classe représentant une demande de trajet.
    """
    def __init__(self, start_coord: tuple[float, float], destination_coord: tuple[float, float]):
        # Coordonnées du point de départ
        start_x, start_y = start_coord
        self.start = Point(start_x, start_y)

        # Coordonnées de la destination
        destination_x, destination_y = destination_coord
        self.destination = Point(destination_x, destination_y)

    def get_route_data_str(self, network: RoadNetwork) -> str:
        data = self.get_route_data(network)
        return "Vous allez passer par les stations " + str(data[0]) + ". Le temps de votre trajet en cabine est estimé à environ " + str(ceil(data[2])) + " min, pour une distance de " + str(ceil(data[1])) + " mètres."

    def get_route_data(self, network: RoadNetwork) -> tuple[list[int], float, float]:
        """
        Connaissant les coordonnées du lieu de départ et celles de la destination, cette méthode va déterminer :
        - la station la plus proche du point de départ
        - la station la plus proche de la destination
         Ainsi, elle sera en mesure de déterminer le chemin que la cabine devra suivre pour emmener l'utilisateur au
         lieu souhaité.
        :return: (le chemin de la cabine pour emmener l'usager au lieu souhaité, sa longueur, la durée du trajet)
        """

        # Détermination de la station de départ et celle d'arrivée
        stations = network.get_nodes()
        start_station = stations[0]
        final_station = stations[0]
        for station in network.get_nodes():
            if Point.get_euclidian_distance(self.start, station) < Point.get_euclidian_distance(self.start, start_station):
                start_station = station
            if Point.get_euclidian_distance(self.destination, station) < Point.get_euclidian_distance(self.destination, final_station):
                final_station = station

        # Calcul du plus court chemin pour aller de la station de départ jusqu'à la station d'arrivée
        path = network.pathfinder(start_station.get_id(), final_station.get_id(), Point.get_euclidian_distance)[0]
        total_distance = network.path_weight(path)
        time = network.time(path)

        return network.parse_nodes_by_id(path), total_distance, time


class GondolaManager:
    """
    Classe représentant le gestionnaire de cabines.
    Se charge de la répartition des cabines en fonction des demandes des usagers.
    """
    def __init__(self, gondola: int, city_map: Map):
        self.number_of_gondola = gondola
        self.city_map = city_map

    def move_gondola(self, start_station_id: int, destination_station_id: int) -> None:
        db = self.city_map.db

        start_station = self.city_map.get_station_by_id(start_station_id)
        start_station.remove_gondola()
        db.set("UPDATE stations WHERE id = " + str(start_station_id) + " SET current_gondola = ...") # TODO: complete req

        destination_station = self.city_map.get_station_by_id(destination_station_id)
        destination_station.add_gondola()

    def handle_request(self, request_data: tuple[list[int], float, float], network: RoadNetwork) -> None:
        """
        TODO: terminer cette fonction...
        V1 !!
        La demande d'un trajet correspond à un événement. L'envoi d'une cabine vers la station de départ constitue la
        réponse de cet événement. Cette dernière ne se fait pas au hasard, et doit nécessiter un temps d'attente
        minimal.

        L'algorithme calcule 3 possibilités, et devra choisir celle qui nécessite le moins de temps d'attente :
        - déplacement d'une cabine de la gare centrale vers la station dans laquelle sera l'usager
        - repérage des stations dans lesquelles il y a des cabines "vides", c'est à dire non utilisées.
          Parmi ces stations, on choisit celle qui est la plus proche de celle où l'usager sera, et on y "extrait" une
          cabine non utilisée.
        - si parmi tous les trajets planifiés, il y en a au moins un qui a pour destination la station dans laquelle
          sera l'usager, alors on l'attend.

        Pour la réponse, il faut connaître :
        - les données de la demande (notamment la station de départ)
        - le réseau, pour pouvoir déplacer une cabine vers la station de départ (à l'aide du graphe donc...)
        - la base de donnée, pour pouvoir effectuer les meilleurs choix en fonction de l'état actuel du réseau de
        transport.

        dictionnaire duree d'attente, chemin menant la cabine à la station de départ
        :return:
        """
        db = self.city_map.db
        x = {}
        # On détermine le noeud de départ du trajet planifié
        route_start_node_id = request_data[0][0]

        # 1. On regarde s'il est possible d'y envoyer une cabine venant de la gare centrale
        main_station_id = db.get("SELECT id FROM stations WHERE is_main = 1")
        main_station = self.city_map.get_station_by_id(main_station_id)
        central_to_start = None
        if main_station.current_gondola > 0:
            central_to_start = network.pathfinder(main_station_id, route_start_node_id, Point.get_euclidian_distance)[0]
            t1 = network.time(central_to_start)
        else:
            t1 = float("inf")
        x[t1] = central_to_start

        # 2. On détermine les stations dans lequelles des cabines sont en attente pour pouvoir déterminer depuis laquelle on a un temps d'attente minimal
        t2 = float("inf")
        stations_waiting_gondola = db.get("SELECT id FROM stations WHERE current_gondola > 0")
        station_to_start = None
        for station in stations_waiting_gondola:
            station_id = station[0]
            station_to_start = network.pathfinder(station_id, route_start_node_id, Point.get_euclidian_distance)[0]
            if network.time(station_to_start) < t2:
                t2 = network.time(station_to_start)
        x[t2] = station_to_start

        req = db.get("SELECT min(time) FROM scheduled_routes GROUP BY destination_id WHERE destination_id = " + str(route_start_node_id) + ";")
