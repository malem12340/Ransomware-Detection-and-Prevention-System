from db import Database


class Dashboard:

    def get_dashboard_data(self):

        db = Database()

        # ==========================================
        # TOTAL FILES MONITORED
        # ==========================================

        db.execute("""
            SELECT COUNT(DISTINCT file_path) AS total
            FROM file_events
        """)

        result = db.fetchone()
        monitored = result["total"] if result else 0

        db.cursor.fetchall()


        # ==========================================
        # RAPID FILE CHANGES
        # ==========================================

        db.execute("""
            SELECT COUNT(*) AS total
            FROM file_events
            WHERE event_type = 'Modified'
        """)

        result = db.fetchone()
        rapid_changes = result["total"] if result else 0

        db.cursor.fetchall()


        # ==========================================
        # TOTAL ALERTS
        # ==========================================

        db.execute("""
            SELECT COUNT(*) AS total
            FROM alerts
        """)

        result = db.fetchone()
        alerts = result["total"] if result else 0

        db.cursor.fetchall()


        # ==========================================
        # TOTAL LOGS
        # ==========================================

        db.execute("""
            SELECT COUNT(*) AS total
            FROM logs
        """)

        result = db.fetchone()
        logs = result["total"] if result else 0

        db.cursor.fetchall()


        # ==========================================
        # TOTAL BACKUPS
        # ==========================================

        db.execute("""
            SELECT COUNT(*) AS total
            FROM backup_history
        """)

        result = db.fetchone()
        backups = result["total"] if result else 0

        db.cursor.fetchall()


        # ==========================================
        # RECENT LOGS
        # ==========================================

        db.execute("""
            SELECT
                username,
                action,
                log_time
            FROM logs
            ORDER BY log_time DESC
            LIMIT 5
        """)

        recent_logs = db.fetchall()


        # ==========================================
        # RECENT ALERTS
        # ==========================================

        db.execute("""
            SELECT
                alert_type,
                severity,
                description,
                alert_time
            FROM alerts
            ORDER BY alert_time DESC
            LIMIT 5
        """)

        recent_alerts = db.fetchall()


        # ==========================================
        # RECENT FILE EVENTS
        # ==========================================

        db.execute("""
            SELECT
                id,
                file_path,
                event_type,
                event_time,
                status
            FROM file_events
            ORDER BY id DESC
            LIMIT 10
        """)

        recent_file_events = db.fetchall()


        # ==========================================
        # SYSTEM STATUS
        # ==========================================

        db.execute("""
            SELECT status
            FROM system_status
            WHERE id = 1
        """)

        result = db.fetchone()

        if result:
            system_status = result["status"]
        else:
            system_status = "SAFE"

        db.cursor.fetchall()


        # ==========================================
        # CHART DATA
        # ==========================================

        db.execute("""
            SELECT
                event_type,
                COUNT(*) AS total
            FROM file_events
            GROUP BY event_type
        """)

        chart_data = db.fetchall()


        # ==========================================
        # CLOSE DATABASE
        # ==========================================

        db.close()


        # ==========================================
        # RETURN ALL DASHBOARD DATA
        # ==========================================

        return {
            "monitored": monitored,
            "rapid_changes": rapid_changes,
            "alerts": alerts,
            "logs": logs,
            "backups": backups,
            "recent_logs": recent_logs,
            "recent_alerts": recent_alerts,
            "recent_file_events": recent_file_events,
            "system_status": system_status,
            "chart_data": chart_data
        }