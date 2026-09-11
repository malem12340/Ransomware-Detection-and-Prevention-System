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
from modules.email_alert import EmailAlert

import os


# ---------------------------------------
# Initialize Components
# ---------------------------------------

detector = DetectionEngine()
alert = AlertManager()
email_alert = EmailAlert()
logger = Logger()
backup = BackupManager()
system = SystemManager()
extension_detector = ExtensionDetector()
event_filter = EventFilter()


# ---------------------------------------
# Monitoring Handler
# ---------------------------------------

class MonitorHandler(FileSystemEventHandler):

    def save_event(self, event_type, path):

        if not event_filter.allow_event(event_type, path):
            return

        # ---------------------------------------
        # Connect to Database
        # ---------------------------------------

        db = Database()

        try:

            # ---------------------------------------
            # Get Next File Event ID
            # ---------------------------------------

            db.execute("""
                SELECT COALESCE(MAX(id), 0) + 1 AS next_id
                FROM file_events
            """)

            result = db.fetchone()

            next_id = result["next_id"] if result else 1

            db.cursor.fetchall()


            # ---------------------------------------
            # Save Event to Database
            # ---------------------------------------

            query = """
            INSERT INTO file_events
            (id, event_type, file_path, event_time, status)
            VALUES (%s, %s, %s, NOW(), %s)
            """

            values = (
                next_id,
                event_type,
                path,
                "Detected"
            )

            db.execute(query, values)


            # ---------------------------------------
            # Suspicious Extension Detection
            # ---------------------------------------

            if extension_detector.is_suspicious(path):

                print("⚠ Suspicious Extension Detected")

                system.set_status("CRITICAL")

                description = (
                    f"Encrypted file detected: "
                    f"{os.path.basename(path)}"
                )


                # Save alert
                alert.create_alert(
                    "Suspicious Extension",
                    description,
                    "Critical"
                )


                # Save log
                logger.save_log(
                    "SYSTEM",
                    "Suspicious extension detected"
                )


                # Send email
                email_alert.send_alert(
                    "Suspicious Extension",
                    description,
                    "Critical"
                )


            # ---------------------------------------
            # Rapid Change Detection
            # ---------------------------------------

            if detector.check():

                if system.can_trigger():

                    print("⚠ RANSOMWARE SUSPECTED")

                    system.set_status("CRITICAL")

                    description = (
                        "Multiple files changed within a short "
                        "period. Possible ransomware activity detected."
                    )


                    # Save alert
                    alert.create_alert(
                        "Rapid File Modification",
                        description,
                        "Critical"
                    )


                    # Save log
                    logger.save_log(
                        "SYSTEM",
                        "Possible ransomware detected"
                    )


                    # Send email
                    email_alert.send_alert(
                        "Rapid File Modification",
                        description,
                        "Critical"
                    )


                    # Create backup
                    backup.backup_all_files(
                        "monitored_folder"
                    )


        except Exception as e:

            print("Database Error:", e)


        finally:

            # ---------------------------------------
            # Close Database
            # ---------------------------------------

            db.close()


        print(event_type, path)


    # ---------------------------------------
    # File Created
    # ---------------------------------------

    def on_created(self, event):

        if not event.is_directory:

            self.save_event(
                "Created",
                event.src_path
            )


    # ---------------------------------------
    # File Modified
    # ---------------------------------------

    def on_modified(self, event):

        if not event.is_directory:

            self.save_event(
                "Modified",
                event.src_path
            )


    # ---------------------------------------
    # File Deleted
    # ---------------------------------------

    def on_deleted(self, event):

        if not event.is_directory:

            self.save_event(
                "Deleted",
                event.src_path
            )


    # ---------------------------------------
    # File Renamed
    # ---------------------------------------

    def on_moved(self, event):

        if not event.is_directory:

            self.save_event(
                "Renamed",
                event.dest_path
            )


# ---------------------------------------
# Start Monitoring
# ---------------------------------------

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