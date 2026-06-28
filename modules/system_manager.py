from db import Database
import time


class SystemManager:

    def __init__(self):

        self.cooldown = 30
        self.last_detection = 0

    def can_trigger(self):

        current = time.time()

        if current - self.last_detection >= self.cooldown:

            self.last_detection = current
            return True

        return False

    def set_status(self, status):

        status = status.upper()

        if status not in ["SAFE", "WARNING", "CRITICAL"]:
            return

        db = Database()

        query = """
        UPDATE system_status
        SET status=%s
        WHERE id=1
        """

        db.execute(query, (status,))
        db.close()

    def get_status(self):

        db = Database()

        query = """
        SELECT status
        FROM system_status
        WHERE id=1
        """

        db.execute(query)

        status = db.fetchone()["status"]

        db.close()

        return status

    def reset_status(self):

        self.set_status("SAFE")