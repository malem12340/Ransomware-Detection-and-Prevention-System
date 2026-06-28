from db import Database


class Logger:

    def save_log(self, username, action):

        db = Database()

        query = """
        INSERT INTO logs(username, action)
        VALUES(%s,%s)
        """

        values = (
            username,
            action
        )

        db.execute(query, values)

        db.close()