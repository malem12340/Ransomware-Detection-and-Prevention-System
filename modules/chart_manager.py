from db import Database


class ChartManager:

    def get_chart_data(self):

        db = Database()

        query = """
        SELECT event_type,
               COUNT(*) AS total
        FROM file_events
        GROUP BY event_type
        """

        db.execute(query)

        data = db.fetchall()

        db.close()

        return data