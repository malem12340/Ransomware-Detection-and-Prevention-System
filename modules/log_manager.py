from db import Database


class LogManager:

    def get_count(self):

        db = Database()

        db.execute("SELECT COUNT(*) AS total FROM logs")

        total = db.fetchone()["total"]

        db.close()

        return total

    def get_recent_logs(self, limit=5):

        db = Database()

        query = """
        SELECT username,
               action,
               log_time
        FROM logs
        ORDER BY log_time DESC
        LIMIT %s
        """

        db.execute(query, (limit,))

        data = db.fetchall()

        db.close()

        return data