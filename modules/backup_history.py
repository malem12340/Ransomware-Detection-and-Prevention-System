from db import Database


class BackupHistory:

    def get_recent_backups(self):

        db = Database()

        query = """
        SELECT *
        FROM backup_history
        ORDER BY backup_time DESC
        LIMIT 10
        """

        db.execute(query)

        data = db.fetchall()

        db.close()

        return data