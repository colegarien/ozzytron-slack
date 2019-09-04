import os
import sqlite3

class DB():
    def __init__(self):
        self.file = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
        self.connection = None
    
    def openConnection(self):
        if self.connection == None:
            self.connection = sqlite3.connect(self.file)
            self.connection.row_factory = sqlite3.Row

    def selectAll(self, query, binds=None):
        return self.execute(query, binds).fetchall()

    def selectOne(self, query, binds=None):
        return self.execute(query, binds).fetchone()

    def insert(self, query, binds=None):
        return self.execute(query, binds).lastrowid

    def execute(self, query, binds=None):
        self.openConnection()
        cursor = self.connection.cursor()
        if binds != None:
            cursor.execute(query, binds)
        else:
            cursor.execute(query)
        self.connection.commit()
        return cursor

if __name__ == "__main__":
    db = DB()
    if os.path.exists(db.file):
        os.remove(db.file)
    db.execute("""
CREATE TABLE player (
    id integer PRIMARY KEY,
    username text NOT NULL,
    ozzy_tokens integer NOT NULL
)
    """)

