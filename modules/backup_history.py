from db import Database


class BackupHistory:

    def get_recent_backups(self):

        db = Database()

        try:

            query = """
            SELECT *
            FROM backup_history
            ORDER BY backup_time DESC
            LIMIT 10
            """

            db.execute(query)

            data = db.fetchall()

            return data

        except Exception as e:

            print("Backup history error:", e)

            return []

        finally:

            db.close()

