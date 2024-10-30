import sqlite3

class Database:
    def __init__(self, path_to_db="database.db"):
        self.path_to_db = path_to_db

    def create_table(self):
        with sqlite3.connect(self.path_to_db) as conn:
            cursor = conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS homework (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                ggroup TEXT,
                homework INTEGER,
                link TEXT 
            )""")
            conn.commit()

    def execute(self, query: str, params: tuple = ()):
        with sqlite3.connect(self.path) as connection:
            connection.execute(query, params)
            connection.commit()