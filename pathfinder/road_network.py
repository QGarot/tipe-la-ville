from math import sqrt
from typing import Self


class Node:
    """
    Classe permettant de représenter un noeud d'un graphe.
    Dans le cadre de l'étude de l'algorithme A*, un noeud possèdera différentes propriétés (toutes initialisées à 0)
    telles que :
        - le coût de déplacement
        - l'heuristique
        - le noeud parent
    """
    def __init__(self, id: int, x: int, y: int):
        # Identifiant
        self.id = id
        # Coordonnées
        self.x = x
        self.y = y
        # Propriétés
        self.g = None
        self.h = None
        self.parent_node = None

    @classmethod
    def get_highest_heuristic_node(cls, n1: Self, n2: Self) -> Self:
        """
        :param n1:
        :param n2:
        :return: Retourne le noeud possédant la valeur de f la plus petite
        """
        f1 = n1.get_f()
        f2 = n2.get_f()
        if f1 < f2:
            return n1
        else:
            return n2

    @classmethod
    def parse_nodes_by_id(cls, nodes: list[Self]):
        """
        :param nodes:
        :return: Retourne la liste des identifiants de chaque noeud composant la liste 'nodes' entré en paramètre
        """
        return [node.get_id() for node in nodes]

    def get_id(self) -> int:
        """
        :return: Retourne l'identifiant de ce noeud
        """
        return self.id

    def get_x(self) -> int:
        """
        :return: Retourne la cordonnées x (abscisse) de ce noeud
        """
        return self.x

    def get_y(self) -> int:
        """
        :return: Retourne la cordonnées y (ordonnée) de ce noeud
        """
        return self.y

    def get_cost(self) -> int | None:
        """
        :return: Retourne le coût associé à ce noeud
        """
        return self.g

    def get_heuristic(self) -> float:
        """
        :return: Retourne l'heuristique associée à ce noeud
        """
        return self.h

    def get_f(self) -> float:
        """
        :return: Retourne la somme du coût et de l'heuristique
        """
        return self.get_heuristic() + self.get_cost()

    def get_parent_node(self) -> Self:
        """
        :return: Retourne le noeud parent, ie le noeud duquel on vient pour arriver à CE noeud
        """
        return self.parent_node


class PriorityQueue:
    def __init__(self, get_highest_priority_element: callable):
        self.get_highest_priority_element = get_highest_priority_element
        self.content = []

    def add(self, x: Node) -> None:
        """
        Ajoute un élément au contenu de la file de priorité
        :param x:
        :return:
        """
        self.content.append(x)

    def pull(self) -> Node:
        """
        :return: Retourne l'élément possédant la plus grande priorité
        """
        highest = self.content[0]
        for element in self.content:
            highest = self.get_highest_priority_element(highest, element)
        self.content.remove(highest)
        return highest

    def is_empty(self) -> bool:
        """
        :return: Retourne True si la file est vide, False sinon
        """
        return len(self.content) == 0

    def in_queue(self, x: Node) -> bool:
        """
        Retourne True si l'élément x est déjà dans la file de priorité, False sinon
        :param x:
        :return:
        """
        return x in self.content


class RoadNetwork:
    """
    Classe représentant un réseau routier, ie un ensemble de routes.
    Un objet de type 'réseau routier' peut être instancié grâce à :
        - un ensemble de points, appelés noeuds (possèdant donc des coordonnées) correspondant à des intersections de routes, des
        stations, etc.
        - une matrice d'adjacence permettant d'établir les liaisons entre les différents noeuds.
    """
    def __init__(self, nodes: list[Node], adjacency_matrix: list[list[float]]):
        self.nodes = nodes
        self.matrix = adjacency_matrix
        self.network = None
        self.set_network_matrix()

    @staticmethod
    def get_distance(n1: Node, n2: Node):
        dx = n2.get_x() - n1.get_x()
        dy = n2.get_y() - n1.get_y()
        return sqrt(dx ** 2 + dy ** 2)

    @staticmethod
    def get_manhattan_distance(n1: Node, n2: Node):
        dx = abs(n2.get_x() - n1.get_x())
        dy = abs(n2.get_y() - n1.get_y())
        return dx + dy

    def get_adjacency_matrix(self) -> list[list[float]]:
        """
        :return: Retourne la matrice d'adjacence permettant de décrire les liaisons entre les différents noeuds
        """
        return self.matrix

    def get_nodes(self) -> list[Node]:
        """
        :return: Retourne la liste des noeuds composant ce réseau
        """
        return self.nodes

    def get_node_by_id(self, id: int) -> Node | None:
        """
        :param id: identifiant du noeud recherché
        :return: Retourne le noeud possedant l'identifiant demandé
        """
        for node in self.get_nodes():
            if node.get_id() == id:
                return node

        return None

    def set_network_matrix(self) -> None:
        """
        Initialise la matrice network, notée M, telle que :
        Quelque soit (i, j) deux identifiants de noeuds,
        - Si i et j correspondent à deux noeuds liés, alors M[i][j] est la distance les séparant
        - Si i = j, M[i][j] vaut 0
        - Si i et j correspondent à des noeuds non liés, alors M[i][j] vaut + l'infini (inf).
        """
        self.network = []
        n = len(self.get_adjacency_matrix())
        for i in range(n):
            line = []
            for j in range(n):
                if self.get_adjacency_matrix()[i][j] == 1:
                    node_i = self.get_node_by_id(i + 1)
                    node_j = self.get_node_by_id(j + 1)
                    distance = self.get_distance(node_i, node_j)
                    line.append(distance)
                else:
                    if i == j:
                        line.append(0)
                    else:
                        line.append(float("inf"))
            self.network.append(line)

    def get_network(self) -> list[list[float]]:
        """
        :return: Retourne la matrice représentant le réseau de transport.
        """
        return self.network

    def get_neighbors(self, node: Node) -> list[Node]:
        """
        :param node:
        :return: Retourne la liste des voisins du noeud choisi
        """
        # i est la ligne de la matrice d'adjacence correspondant au noeud d'identifiant i.
        i = node.get_id() - 1
        neighbors = []
        for j in range(len(self.get_adjacency_matrix())):
            if self.get_adjacency_matrix()[i][j] == 1:
                neighbors.append(self.get_node_by_id(j + 1))

        return neighbors

    def build_path_to(self, start: Node, final: Node) -> list[Node]:
        """
        Construit récursivement le chemin allant de 'final' à 'start'.
        :param final:
        :param start:
        :return: Retourne la liste de noeuds construite récursivement correspondant à ce chemin.
        """
        if final == start:
            return [final]
        else:
            res = self.build_path_to(start, final.get_parent_node())
            res.append(final)
            return res

    def weight(self, n1: Node, n2: Node):
        """
        :param n1:
        :param n2:
        :return: Retourne le poids de l'arête partant de n1 jusqu'à n2.
        """
        return self.get_network()[n1.get_id() - 1][n2.get_id() - 1]

    def pathfinder(self, start_id: int, goal_id: int) -> list[int]:
        """
        Première version du pathfinder.
        :param start_id:
        :param goal_id:
        :return: le chemin le plus court allant du noeud ayant pour id start_id au noeud ayant pour id goal_id
        """
        # Création de la file de priorité
        prio_queue = PriorityQueue(Node.get_highest_heuristic_node)

        # Initialisation des propriétés du noeud de départ
        start = self.get_node_by_id(start_id)
        goal = self.get_node_by_id(goal_id)
        start.g = 0
        start.h = self.get_manhattan_distance(start, goal)

        # Ajout du noeud de départ à la file de priorité
        prio_queue.add(start)

        # Initialisation du noeud courant :
        u = start
        while u != goal and not prio_queue.is_empty():
            u = prio_queue.pull()
            for neighbor in self.get_neighbors(u):
                new_cost = u.get_cost() + self.weight(u, neighbor)
                if neighbor.get_cost() is None or new_cost < neighbor.get_cost():
                    # Mise à jour du coût de déplacement, du noeud parent et que l'heuristique
                    neighbor.g = new_cost
                    neighbor.parent_node = u
                    neighbor.h = self.get_manhattan_distance(neighbor, goal)
                    # Ajout de ce voisin dans la file de priorité
                    if not prio_queue.in_queue(neighbor):
                        prio_queue.add(neighbor)

        if u == goal:
            return Node.parse_nodes_by_id(self.build_path_to(start, u))
        else:
            return []
