import mysql.connector


class Database:
    def __init__(self, host, user, password, name):
        self.host = host
        self.user = user
        self.password = password
        self.name = name

        self.connection = None
        self.cursor = None

    def prepare_db(self):
        """
        Méthode permettant de se connecter à la base de données et de positionner l'objet curseur.
        A appeler avant chaque action !
        :return:
        """
        self.connection = mysql.connector.connect(
            host=self.host,
            port=3306,
            user=self.user,
            database=self.name,
            password=self.password
        )

        self.cursor = self.connection.cursor()

    def close_connection(self):
        """
        Méthode permettant de fermer la connexion à la base de données et le curseur.
        A appeler après chaque action !
        :return:
        """
        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None

    def get(self, sql: str) -> list[tuple]:
        """
        Permet de récupérer des informations contenues dans la base de données.
        :param sql:
        :return: n-tuple
        """
        self.prepare_db()
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.close_connection()
        return result

    def set(self, sql: str) -> None:
        """
        Permet d'effectuer une action sur la base de données (insertion, modification, suppression).
        :param sql:
        :return:
        """
        self.prepare_db()

        self.cursor.execute(sql)
        self.connection.commit()

        self.close_connection()
