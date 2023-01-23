class Platform:
    """
    Une station est composée de plusieurs plateformes, chacune d'entre elles permettant de prendre un supras pour se
    rendre à une station voisine (ie reliée à notre station de départ).

    Exemple :
    On suppose qu'un noeud A est relié à un noeud B et à un noeud C.
    Alors A comporte 2 plateformes, une permettant d'aller en B et l'autre permettant d'aller en C.
    """
    def __init__(self, id, station_id, target_platform_id, current_people, is_open):
        self.id = id
        self.station_id = station_id
        self.target_platform_id = target_platform_id
        self.current_people = current_people
        self.is_open = is_open

    @classmethod
    def generate_with_adjacency_matrix(cls, db, matrix):
        """
        Permet d'insérer dans la base de données les informations relatives aux plateformes de chaque station à partir
        de la matrice d'adjacence.
        :param db:
        :param matrix:
        :param platforms_set:
        :return:
        """
        current_id = 1
        # La matrice d'adjacence étant symétrique, on peut
        #   1. éviter de parcourir tous les éléments de la matrice
        #   2. directement déduire l'existence de 2 plateformes
        n = len(matrix)
        for i in range(n):
            for j in range(i, n):
                if matrix[i][j] == 1:
                    db.insert("platforms", "(station_id, target_platform_id)", (i + 1, current_id + 1))
                    db.insert("platforms", "(station_id, target_platform_id)", (j + 1, current_id))
                    current_id = current_id + 2
