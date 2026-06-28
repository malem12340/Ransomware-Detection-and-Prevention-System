import os
import shutil

from db import Database


class RestoreManager:

    def get_all_backups(self):

        db = Database()

        query = """
        SELECT *
        FROM backup_history
        ORDER BY backup_time DESC
        """

        db.execute(query)

        data = db.fetchall()

        db.close()

        return data

    def restore_file(self, backup_file):

        source = os.path.join("backups", backup_file)

        destination = os.path.join("monitored_folder", backup_file)

        if not os.path.exists(source):
            return False

        shutil.copy2(source, destination)

        return True