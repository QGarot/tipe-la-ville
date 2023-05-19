from math import sqrt
from typing import Self
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def get_x(self) -> float:
        return self.x

    def get_y(self) -> float:
        return self.y

    @classmethod
    def get_euclidian_distance(cls, p1: Self, p2: Self) -> float:
        dx = p2.get_x() - p1.get_x()
        dy = p2.get_y() - p1.get_y()
        return sqrt(dx ** 2 + dy ** 2) * 50 / 8

    @classmethod
    def get_manhattan_distance(cls, n1: Self, n2: Self) -> float:
        dx = abs(n2.get_x() - n1.get_x())
        dy = abs(n2.get_y() - n1.get_y())
        return (dx + dy) * 50 / 8

    @classmethod
    def heuristic_null(cls, n1: Self, n2: Self) -> float:
        return 0


class Node(Point):
    """
    Classe permettant de représenter un noeud d'un graphe.
    Dans le cadre de l'étude de l'algorithme A*, un noeud possèdera différentes propriétés (toutes initialisées à None)
    telles que :
        - le coût de déplacement
        - l'heuristique
        - le noeud parent
    """
    def __init__(self, id: int, x: int, y: int):
        # Identifiant
        super().__init__(x, y)
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

    def get_id(self) -> int:
        """
        :return: Retourne l'identifiant de ce noeud
        """
        return self.id

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

    def set_cost(self, cost: float | None) -> None:
        """
        Attribue la valeur 'cost' à 'g'
        :param cost:
        """
        self.g = cost

    def set_heuristic(self, heuristic: float | None) -> None:
        """
        Attribue la valeur 'heuristic' à 'h'
        :param heuristic:
        :return:
        """
        self.h = heuristic

    def set_parent_node(self, node: Self | None) -> None:
        """
        Attribue un nouveau noeud parent
        :param node:
        :return:
        """
        self.parent_node = node

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

    def has(self, x: Node) -> bool:
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
        - un ensemble de points, appelés noeuds (possèdant donc des coordonnées) correspondant ici à des stations.
        - une matrice d'adjacence permettant d'établir les liaisons entre les différents noeuds.
    """
    def __init__(self, nodes: list[Node], adjacency_matrix: list[list[float]]):
        self.nodes = nodes
        self.matrix = adjacency_matrix

        self.network = None
        self.set_network_matrix()

    @classmethod
    def parse_nodes_by_id(cls, nodes: list[Node]) -> list[int]:
        """
        :param nodes:
        :return: Retourne la liste des identifiants de chaque noeud composant la liste 'nodes' entrée en paramètre
        """
        return [node.get_id() for node in nodes]

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
                    distance = Point.get_euclidian_distance(node_i, node_j)
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

    def weight(self, n1: Node, n2: Node) -> float:
        """
        :param n1:
        :param n2:
        :return: Retourne le poids de l'arête partant de n1 jusqu'à n2.
        """
        return self.get_network()[n1.get_id() - 1][n2.get_id() - 1]

    def path_weight(self, nodes: list[Node]) -> float:
        """
        Calcule le poids d'un chemin, défini comme la somme des poids des arêtes qui le composent.
        :param nodes:
        :return: Retourne la valeur du poids du chemin désigné par la liste 'nodes' entrée en paramètre.
        """
        n = len(nodes)
        res = 0
        for k in range(n - 1):
            res = res + self.weight(nodes[k], nodes[k + 1])
        return res

    def reset_nodes_properties(self) -> None:
        """
        Ré-initialise les propriétés de chaque noeud. Cette methode doit être appelée avant la recherche d'un plus
        court chemin, pour s'assurer de bien initialiser correctement toutes les propriétés de chaque noeud.
        :return:
        """
        for node in self.get_nodes():
            node.set_parent_node(None)
            node.set_cost(None)
            node.set_heuristic(None)

    def pathfinder(self, start_id: int, goal_id: int, heuristic: callable) -> tuple[list[Node], float]:
        """
        Implémentation de l'algorithme A*.
        :param heuristic:
        :param start_id:
        :param goal_id:
        :return: un couple de la forme :
        (le chemin le plus court allant du noeud ayant pour id 'start_id' au noeud ayant pour id 'goal_id', tours de boucle)
        """
        # Element d'analyse
        t = 0

        # Création de la file de priorité
        prio_queue = PriorityQueue(Node.get_highest_heuristic_node)

        # Initialisation des propriétés du noeud de départ
        start = self.get_node_by_id(start_id)
        goal = self.get_node_by_id(goal_id)
        start.set_cost(0)
        start.set_heuristic(heuristic(start, goal))

        # Ajout du noeud de départ à la file de priorité
        prio_queue.add(start)

        # Initialisation du noeud actuel :
        u = start
        while u != goal and not prio_queue.is_empty():
            u = prio_queue.pull()
            for neighbor in self.get_neighbors(u):
                new_cost = u.get_cost() + self.weight(u, neighbor)
                if neighbor.get_cost() is None or new_cost < neighbor.get_cost():
                    # Mise à jour du coût de déplacement, du noeud parent et que l'heuristique
                    neighbor.set_cost(new_cost)
                    neighbor.set_parent_node(u)
                    neighbor.set_heuristic(heuristic(neighbor, goal))
                    # Ajout de ce voisin dans la file de priorité
                    if not prio_queue.has(neighbor):
                        prio_queue.add(neighbor)
            t = t + 1

        if u == goal:
            return self.build_path_to(start, u), t
        else:
            return [], t

    def compare(self, start_node_id: int, final_node_id: int, heuristics: list[callable], colors: list[str]) -> None:
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
            path_info = self.pathfinder(start_node_id, final_node_id, heuristic)
            loops_number = path_info[1]
            # print(path_info[0])
            self.reset_nodes_properties()
            heuristic_names.append(heuristic.__name__)
            loops_set.append(loops_number)

        ax.bar(heuristic_names, loops_set, color=colors)
        ax.set_ylabel("Nombre de tours de boucle")
        ax.set_title("Efficacité du pathfinder selon l'heuristique choisie")
        plt.show()
