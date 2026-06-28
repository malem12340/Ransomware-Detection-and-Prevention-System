from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from db import Database

from modules.detection import DetectionEngine
from modules.alerts import AlertManager
from modules.logger import Logger
from modules.backup import BackupManager
from modules.system_manager import SystemManager
from modules.extension_detector import ExtensionDetector
from modules.event_filter import EventFilter

import os
import time



detector = DetectionEngine()
alert = AlertManager()
logger = Logger()
backup = BackupManager()
system = SystemManager()
extension_detector = ExtensionDetector()
event_filter = EventFilter()


class MonitorHandler(FileSystemEventHandler):

    def save_event(self, event_type, path):
        
        if not event_filter.allow_event(event_type, path):
            return

        # ---------------------------------------
        # Save Event to Database
        # ---------------------------------------

        db = Database()

        query = """
        INSERT INTO file_events
        (event_type, file_name, file_path)
        VALUES (%s, %s, %s)
        """

        values = (
            event_type,
            os.path.basename(path),
            path
        )

        db.execute(query, values)

        # ---------------------------------------
        # Suspicious Extension Detection
        # ---------------------------------------

        if extension_detector.is_suspicious(path):

            print("⚠ Suspicious Extension Detected")

            system.set_status("CRITICAL")

            alert.create_alert(
                "Suspicious Extension",
                f"Encrypted file detected: {os.path.basename(path)}",
                "Critical"
            )

            logger.save_log(
                "SYSTEM",
                "Suspicious extension detected"
            )

        # ---------------------------------------
        # Rapid Change Detection
        # ---------------------------------------

        if detector.check():

            if system.can_trigger():

                print("⚠ RANSOMWARE SUSPECTED")

                system.set_status("CRITICAL")

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

    # ---------------------------------------
    # File Created
    # ---------------------------------------

    def on_created(self, event):

        if not event.is_directory:
            self.save_event("Created", event.src_path)

    # ---------------------------------------
    # File Modified
    # ---------------------------------------

    def on_modified(self, event):

        if not event.is_directory:
            self.save_event("Modified", event.src_path)

    # ---------------------------------------
    # File Deleted
    # ---------------------------------------

    def on_deleted(self, event):

        if not event.is_directory:
            self.save_event("Deleted", event.src_path)

    # ---------------------------------------
    # File Renamed
    # ---------------------------------------

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