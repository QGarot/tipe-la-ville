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


class PriorityQueue(list[Node]):
    def __init__(self, get_highest_priority_element: callable):
        super().__init__()
        self.get_highest_priority_element = get_highest_priority_element

    def add(self, x: Node) -> None:
        """
        Ajoute un élément au contenu de la file de priorité
        :param x:
        :return:
        """
        self.append(x)

    def pull(self) -> Node:
        """
        :return: Retourne l'élément possédant la plus grande priorité
        """
        highest = self[0]
        for element in self:
            highest = self.get_highest_priority_element(highest, element)
        self.remove(highest)
        return highest

    def is_empty(self) -> bool:
        """
        :return: Retourne True si la file est vide, False sinon
        """
        return len(self) == 0


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

    @staticmethod
    def get_distance(n1: Node, n2: Node):
        dx = n2.get_x() - n1.get_x()
        dy = n2.get_y() - n1.get_y()
        return sqrt(dx ** 2 + dy ** 2)

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

    @staticmethod
    def get_highest_heuristic_node(n1: Node, n2: Node) -> Node:
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

    @staticmethod
    def filter_path_id(path: list[Node]):
        return [node.get_id() for node in path]

    def get_network_matrix(self) -> list[list[float]]:
        """
        :return: Retourne une matrice M telle que :
        Quelque soit (i, j) deux identifiants de noeuds,
        - Si i et j correspondent à deux noeuds liés, alors M[i][j] est la distance les séparant
        - Si i = j, M[i][j] vaut 0
        - Si i et j correspondent à des noeuds non liés, alors M[i][j] vaut + l'infini (inf).
        """
        res = []
        n = len(self.get_adjacency_matrix())
        for i in range(n):
            line = []
            for j in range(n):
                if self.get_adjacency_matrix()[i][j] == 1:
                    node_i = self.get_node_by_id(i)
                    node_j = self.get_node_by_id(j)
                    distance = self.get_distance(node_i, node_j)
                    line.append(distance)
                else:
                    if i == j:
                        line.append(0)
                    else:
                        line.append(float("inf"))
            res.append(line)
        return res

    def get_neighbors(self, node: Node) -> list[Node]:
        """
        :param node:
        :return: Retourne la liste des voisins du noeud choisi
        """
        i = node.get_id()
        neighbors = []
        for j in range(len(self.get_adjacency_matrix())):
            if self.get_adjacency_matrix()[i][j] == 1:
                neighbors.append(self.get_node_by_id(j))

        return neighbors

    @staticmethod
    def build_path_to(start: Node, final: Node) -> list[Node]:
        """
        Construit le chemin allant de 'node' (entré en paramètre) jusqu'à CE noeud.
        :param final:
        :param start:
        :return: la liste de noeud construite récursivement correspondant à ce chemin.
        Si CE noeud (self) n'est pas le noeud final (node), alors ajouter self à la liste créée récursivement par
        l'appel de build_path_to(node) depuis le parent de self.
        """
        current_node = final
        path = [final]
        while current_node.get_id() != start.get_id():
            current_node = current_node.get_parent_node()
            path.append(current_node)

        path.reverse()
        return path

    def pathfinder(self, start_id: int, goal_id: int) -> list[int]:
        """
        Première version du pathfinder.
        :param start_id:
        :param goal_id:
        :return: le chemin le plus court allant du noeud ayant pour id start_id au noeud ayant pour id goal_id
        """
        network = self.get_network_matrix()
        # Création de la file de priorité
        prio_queue = PriorityQueue(self.get_highest_heuristic_node)
        # Initialisation des propriétés du noeud de départ
        start = self.get_node_by_id(start_id)
        goal = self.get_node_by_id(goal_id)
        start.g = 0
        start.h = self.get_distance(start, goal)
        # Ajout du noeud de départ à la file de priorité
        prio_queue.add(start)
        while not prio_queue.is_empty():
            current = prio_queue.pull()
            if current.get_id() == goal.get_id():
                return self.filter_path_id(self.build_path_to(start, goal))
            else:
                for neighbor in self.get_neighbors(current):
                    new_cost = current.get_cost() + network[current.get_id()][neighbor.get_id()]
                    if neighbor.get_cost() is None or new_cost < neighbor.get_cost():
                        # Mise à jour du coût de déplacement, du noeud parent et que l'heuristique
                        neighbor.g = new_cost
                        neighbor.parent_node = current
                        neighbor.h = self.get_distance(neighbor, goal)
                        # Ajout de ce voisin dans la file de priorité
                        prio_queue.add(neighbor)
