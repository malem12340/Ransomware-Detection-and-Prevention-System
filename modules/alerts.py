from db import Database


class AlertManager:

    def create_alert(self, alert_type, description, severity):

        db = Database()

        query = """
        INSERT INTO alerts
        (alert_type,description,severity)
        VALUES(%s,%s,%s)
        """

        values = (
            alert_type,
            description,
            severity
        )

        db.execute(query, values)

        db.close()