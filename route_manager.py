import time
from pathfinder.road_network import RoadNetwork, Point
from math import ceil
from build_network.map import Station, Map


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
        # print("Chemin : " + str(data[0]))
        # print("Temps de trajet en cabine : ~" + str(ceil(data[2])) + "min")
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

        return network.parse_nodes_by_id(path), network.path_weight(path), network.time(path)


class GondolaManager:
    """
    Classe représentant le gestionnaire de cabines.
    Se charge de la répartition des cabines en fonction des demandes des usagers.
    """
    def __init__(self, gondola: int, city_map: Map):
        self.number_of_gondola = gondola
        self.city_map = city_map

    def move_gondola(self, start_station_id: int, destination_station_id: int) -> None:
        pass

    def handle_request(self, request_data: tuple[list[int], float, float], network: RoadNetwork) -> None:
        """
        V3
        La demande d'un trajet correspond à un événement. L'envoi d'une cabine vers la station de départ constitue la
        réponse de cet événement. Cette dernière ne se fait pas au hasard, et doit nécessiter un temps d'attente
        minimal pour l'usager.

        Le programme calcule 2 possibilités, et devra choisir celle qui nécessite le moins de temps d'attente :
        - On détermine l'ensemble des trajets en cours ayant pour destination la station de départ.
        Pour chacun d'entre eux, on détermine le temps de trajet restant, pour ensuite déterminer le plus petit.
        - On détermine l'ensemble des stations dans lesquelles il y a au moins une cabine non utilisée. On regarde
        si depuis l'une d'entre elles une cabine peut accéder à la station de départ en un temps inférieur.
        Repérage des stations dans lesquelles il y a des cabines "vides", c'est à dire non utilisées.

        Pour la réponse, il faut connaître :
        - les données de la demande (pour connaître la station de départ)
        - le réseau, pour pouvoir déplacer une cabine vers la station de départ (à l'aide du graphe donc...)
        - la base de donnée, pour pouvoir effectuer les meilleurs choix en fonction de l'état actuel du réseau de
        transport.
        :return:
        """
        db = self.city_map.db

        # On détermine le noeud de départ du trajet planifié
        route_start_node_id = request_data[0][0]

        # On definit le temps d'attente t de l'usager, ainsi que le chemin que suivra la cabine pour se rendre à la
        # station souhaitée.
        t = float("inf")
        path = None

        # 1. On détermine les trajets planifiés qui ont pour station d'arrivée la station souhaitée.
        #    MAJ de t : t <- minimum des temps restants de chacun de trajets
        # TODO: mettre à jour la BDD si nécessaire!
        req = db.get("SELECT min(arrival) FROM scheduled_routes WHERE destination_id = " + str(route_start_node_id) + ";")
        if len(req) != 0:
            for scheduled_route in req:
                arrival = scheduled_route[0]  # date d'arrivée
                current_time = time.time()
                temp_t = ceil((arrival - current_time) / 60)
                if temp_t < t:
                    t = temp_t
                    path = None  # Le chemin est en cours... inutile de le renseigner à nouveau

        # 2. On détermine les stations dans lequelles des cabines sont en attente
        #    On regarde si, depuis l'une d'entre elle, la cabine peut acceder à notre station en un temps plus petit
        req = db.get("SELECT id FROM stations WHERE current_gondola > 0;")
        if len(req) != 0:
            for station in req:
                station_id = station[0]
                temp_path = network.pathfinder(station_id, route_start_node_id, Point.get_euclidian_distance)[0]
                temp_t = network.time(temp_path)
                if temp_t < t:
                    t = temp_t
                    path = temp_path

        # Appel de la cabine...
        if path is not None:
            self.move_gondola(path[0].get_id(), path[-1].get_id())
            print("Une cabine vient d'être envoyée... Elle arrive dans environ " + str(t) + " minute(s).")
        else:
            print("Une cabine arrive dans environ " + str(t) + " minute(s).")
