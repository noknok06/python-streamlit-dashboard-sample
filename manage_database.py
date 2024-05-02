import sqlite3

class ManageDatabase:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

    def disconnect_database(self):
        self.conn.close