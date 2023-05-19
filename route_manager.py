from pathfinder.road_network import RoadNetwork, Point


class Queue:
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
    def __init__(self, network: RoadNetwork, start_coord: tuple[float, float], destination_coord: tuple[float, float]):
        self.network = network

        # Coordonnées du point de départ
        start_x, start_y = start_coord
        self.start = Point(start_x, start_y)

        # Coordonnées de la destination
        destination_x, destination_y = destination_coord
        self.destination = Point(destination_x, destination_y)

    def get_route_data(self) -> tuple[list[int], float, float]:
        """
        Connaissant les coordonnées du lieu de départ et celles de la destination, cette méthode va déterminer :
        - la station la plus proche du point de départ
        - la station la plus proche de la destination
         Ainsi, elle sera en mesure de déterminer le chemin que la cabine devra suivre pour emmener l'utilisateur au
         lieu souhaité.
        :return: (le chemin de la cabine pour emmener l'usager au lieu souhaité, sa longueur, la durée du trajet)
        """

        # Détermination de la station de départ et celle d'arrivée
        stations = self.network.get_nodes()
        start_station = stations[0]
        final_station = stations[0]
        for station in self.network.get_nodes():
            if Point.get_euclidian_distance(self.start, station) < Point.get_euclidian_distance(self.start, start_station):
                start_station = station
            if Point.get_euclidian_distance(self.destination, station) < Point.get_euclidian_distance(self.destination, final_station):
                final_station = station

        # Calcul du plus court chemin pour aller de la station de départ jusqu'à la station d'arrivée
        path = self.network.pathfinder(start_station.get_id(), final_station.get_id(), Point.get_euclidian_distance)[0]
        total_distance = self.network.path_weight(path)
        time = total_distance * 60 / 50000

        return self.network.parse_nodes_by_id(path), total_distance, time


class RouteManager:
    def __init__(self):
        pass
