from db import Database


class AlertManagerDB:

    def get_count(self):

        db = Database()

        db.execute("SELECT COUNT(*) AS total FROM alerts")

        total = db.fetchone()["total"]

        db.close()

        return total

    def get_recent_alerts(self, limit=5):

        db = Database()

        query = """
        SELECT alert_type,
               severity,
               description,
               alert_time
        FROM alerts
        ORDER BY alert_time DESC
        LIMIT %s
        """

        db.execute(query, (limit,))

        data = db.fetchall()

        db.close()

        return data