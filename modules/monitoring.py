from modules.alerts import AlertManager
from modules.detection import DetectionEngine
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from modules.system_manager import SystemManager

from modules.logger import Logger

from modules.backup import BackupManager

import time
import os

from db import Database

detector = DetectionEngine()

alert = AlertManager()
logger = Logger()
backup = BackupManager()
system = SystemManager()

class MonitorHandler(FileSystemEventHandler):

    def save_event(self, event_type, path):

        db = Database()

        query = """
        INSERT INTO file_events
        (event_type,file_name,file_path)
        VALUES(%s,%s,%s)
        """

        values = (

            event_type,

            os.path.basename(path),

            path

        )

        db.execute(query, values)

        if detector.check():

            if system.can_trigger():

                print("⚠ RANSOMWARE SUSPECTED")

                system.set_status("CRITICAL")

            def reset_status(self):

                self.set_status("SAFE")

            alert.create_alert(

                "Rapid File Modification",

                "Multiple files changed within a short period. Possible ransomware activity detected.",

                "Critical"
            )

            logger.save_log(

                "SYSTEM",

                "Possible ransomware detected"
            )

            backup.backup_all_files("monitored_folder")

        db.close()

        print(event_type, path)

    # File Created

    def on_created(self, event):

        if not event.is_directory:

            self.save_event("Created", event.src_path)

    # File Modified

    def on_modified(self, event):

        if not event.is_directory:

            self.save_event("Modified", event.src_path)

    # File Deleted

    def on_deleted(self, event):

        if not event.is_directory:

            self.save_event("Deleted", event.src_path)

    # File Renamed

    def on_moved(self, event):

        if not event.is_directory:

            self.save_event("Renamed", event.dest_path)


def start_monitoring():

    folder = "monitored_folder"

    event_handler = MonitorHandler()

    observer = Observer()

    observer.schedule(

        event_handler,

        folder,

        recursive=True

    )

    observer.start()

    print("Monitoring Started...")

    return observer