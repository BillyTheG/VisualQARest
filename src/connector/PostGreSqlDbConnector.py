import psycopg2
from connector.AbstractDbConnector import AbstractDbConnector


class PostGresConnector(AbstractDbConnector):

    def __init__(self, driver, server, database, user, pw, port):
        super().__init__(driver, server, database, user, pw, port)
        self.connection = psycopg2.connect(host=server, database=database, user=user, password=pw, port=int(port))
        self.global_cursor = self.connection.cursor()
