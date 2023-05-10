import mysql.connector


class Database:
    def __init__(self, host, user, password, name):
        """
        Classe permettant de gérer les actions effectuées sur une base de données.
        :param host:
        :param user:
        :param password:
        :param name:
        """
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

    def update(self, table_name, attribute, new_value, sql_condition):
        """
        V1; Permet de mettre à jour les données d'une table.
        :param table_name:
        :param attribute:
        :param new_value:
        :param sql_condition:
        :return:
        """
        self.prepare_db()

        sql = "UPDATE " + table_name + " SET " + attribute + " = '" + new_value + "' WHERE " + sql_condition
        self.cursor.execute(sql)
        self.connection.commit()

        self.close_connection()

    def update2(self, table_name: str, attributes: dict, sql_condition: str):
        """
        V2; Permet de mettre à jour les données d'une table.
        -> {"fied": new value of this field}
        :param table_name:
        :param attributes:
        :param sql_condition:
        :return:
        """
        attr_str = ""
        first = True
        for couple in attributes.items():
            print(couple)
            if first:
                attr_str = attr_str + couple[0] + " = '" + str(couple[1]) + "'"
                first = False
            else:
                attr_str = attr_str + ", " + couple[0] + " = '" + str(couple[1]) + "'"

        self.prepare_db()
        sql = "UPDATE " + table_name + " SET " + attr_str + " WHERE " + sql_condition
        self.cursor.execute(sql)
        self.connection.commit()

        self.close_connection()

    def get(self, sql: str) -> []:
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

    def insert(self, table_name, structure, values):
        """
        Permet d'insérer de nouveaux enregistrements dans une table.
        :param table_name:
        :param structure:
        :param values:
        :return: None
        """

        self.prepare_db()

        sql = "INSERT INTO " + table_name + " " + structure + " VALUES " + str(values)
        self.cursor.execute(sql)
        self.connection.commit()

        self.close_connection()

    def select(self, attributes, table_name, sql_condition=None) -> list:
        """
        Retourne une liste de n-tuples si n champs sont sélectionnés.
        :param sql_condition:
        :param table_name:
        :param attributes:
        :return: list
        """
        self.prepare_db()

        if sql_condition is not None:
            sql = "SELECT " + attributes + " FROM " + table_name + " WHERE " + sql_condition
        else:
            sql = "SELECT " + attributes + " FROM " + table_name
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        self.close_connection()
        return result

    def select_id_of_last_insertion(self, table_name):
        """
        Permet de récuperer l'id du dernier élément inséré dans la table.
        :param table_name:
        :return:
        """
        self.prepare_db()

        sql = "SELECT MAX(id) FROM" + table_name + ";"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        self.close_connection()
        return result[0][0]
