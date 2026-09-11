from db import Database


class AlertManager:

    def create_alert(self, alert_type, description, severity):

        db = Database()

        try:

            # ---------------------------------------
            # Get Next Alert ID
            # ---------------------------------------

            db.execute("""
                SELECT COALESCE(MAX(id), 0) + 1 AS next_id
                FROM alerts
            """)

            result = db.fetchone()

            next_id = result["next_id"] if result else 1

            db.cursor.fetchall()


            # ---------------------------------------
            # Save Alert
            # ---------------------------------------

            query = """
            INSERT INTO alerts
            (id, alert_type, description, severity, alert_time)
            VALUES (%s, %s, %s, %s, NOW())
            """

            values = (
                next_id,
                alert_type,
                description,
                severity
            )

            db.execute(query, values)

            print("✓ Alert saved successfully")

        except Exception as e:

            print("Alert Database Error:", e)

        finally:

            db.close()