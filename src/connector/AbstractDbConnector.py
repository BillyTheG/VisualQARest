from abc import ABC, abstractmethod


class AbstractDbConnector(ABC):
    driver: str
    server: str
    database: str
    user: str
    pw: str
    port: str
    connection: object
    global_cursor: object

    def __init__(self, driver, server, database, user, pw, port):
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.pw = pw
        self.port = port
