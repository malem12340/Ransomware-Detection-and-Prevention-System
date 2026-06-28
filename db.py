import mysql.connector
from config import Config


class Database:

    def __init__(self):

        self.connection = mysql.connector.connect(
            host=Config.DB_HOST,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )

        self.cursor = self.connection.cursor(dictionary=True)

    def execute(self, query, values=None):

        if values:
            self.cursor.execute(query, values)
        else:
            self.cursor.execute(query)

        # Commit ONLY for INSERT, UPDATE, DELETE
        if query.strip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
            self.connection.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()