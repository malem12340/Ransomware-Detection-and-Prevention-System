from db import Database


class Dashboard:

    def get_dashboard_data(self):

        db = Database()

        # -------------------------
        # Dashboard Cards
        # -------------------------

        db.execute("SELECT COUNT(*) AS total FROM alerts")
        alerts = db.fetchone()["total"]
        db.cursor.fetchall()

        db.execute("SELECT COUNT(*) AS total FROM logs")
        logs = db.fetchone()["total"]
        db.cursor.fetchall()

        db.execute("SELECT COUNT(*) AS total FROM backups")
        backups = db.fetchone()["total"]
        db.cursor.fetchall()

        # -------------------------
        # Recent Logs
        # -------------------------

        db.execute("""
            SELECT username, action, log_time
            FROM logs
            ORDER BY log_time DESC
            LIMIT 5
        """)

        recent_logs = db.fetchall()

        # -------------------------
        # Recent Alerts
        # -------------------------

        db.execute("""
                SELECT alert_type,
                severity,
                description,
                alert_time
            FROM alerts
            ORDER BY alert_time DESC
            LIMIT 5
        """)

        recent_alerts = db.fetchall()

        # -------------------------
        # System Status
        # -------------------------

        db.execute("""
            SELECT status
            FROM system_status
            WHERE id=1
        """)

        system_status = db.fetchone()["status"]

        db.cursor.fetchall()

        # -------------------------
        # File Events Chart
        # -------------------------

        db.execute("""

            SELECT event_type, COUNT(*) AS total

            FROM file_events

            GROUP BY event_type
        """)

        chart_data = db.fetchall()

        db.close()

        return {

            "alerts": alerts,

            "logs": logs,

            "backups": backups,

            "recent_logs": recent_logs,

            "recent_alerts": recent_alerts,

            "system_status": system_status,

            "chart_data": chart_data
        }