import sqlite3
from contextlib import contextmanager

class SQLiteManager:
    def __init__(self, db_name):
        self.db_name = db_name

    @contextmanager
    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            yield conn
        except sqlite3.Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
