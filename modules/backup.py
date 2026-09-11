import os
import shutil

from db import Database


class BackupManager:

    # ---------------------------------------
    # Allowed File Types
    # ---------------------------------------

    ALLOWED_EXTENSIONS = (

        ".txt",
        ".pdf",
        ".doc",
        ".docx",
        ".jpg",
        ".png",
        ".xlsx",
        ".pptx"

    )

    BACKUP_FOLDER = "backups"


    # ---------------------------------------
    # Backup Single File
    # ---------------------------------------

    def backup_file(self, file_path):

        if not os.path.exists(file_path):
            return

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            print(
                "Backup skipped - unsupported file:",
                file_path
            )
            return


        # ---------------------------------------
        # Create Backup Folder
        # ---------------------------------------

        os.makedirs(
            self.BACKUP_FOLDER,
            exist_ok=True
        )


        # ---------------------------------------
        # Create Unique Backup Filename
        # ---------------------------------------

        filename = os.path.basename(file_path)

        destination = os.path.join(
            self.BACKUP_FOLDER,
            filename
        )

        # Avoid overwriting existing backup
        if os.path.exists(destination):

            name, ext = os.path.splitext(filename)

            counter = 1

            while os.path.exists(destination):

                new_filename = (
                    f"{name}_backup_{counter}{ext}"
                )

                destination = os.path.join(
                    self.BACKUP_FOLDER,
                    new_filename
                )

                counter += 1


            filename = os.path.basename(destination)


        # ---------------------------------------
        # Copy File
        # ---------------------------------------

        try:

            shutil.copy2(
                file_path,
                destination
            )

        except Exception as e:

            print(
                "Backup failed:",
                file_path,
                e
            )

            return


        # ---------------------------------------
        # Save Backup History
        # ---------------------------------------

        db = Database()

        try:

            # Get next ID because Railway table
            # does not use AUTO_INCREMENT

            db.execute("""
                SELECT COALESCE(MAX(id), 0) + 1 AS next_id
                FROM backup_history
            """)

            result = db.fetchone()

            next_id = (
                result["next_id"]
                if result
                else 1
            )

            db.cursor.fetchall()


            query = """
            INSERT INTO backup_history
            (id, file_name, original_path, backup_path)
            VALUES (%s, %s, %s, %s)
            """

            values = (
                next_id,
                filename,
                file_path,
                destination
            )

            db.execute(
                query,
                values
            )

            print(
                "✓ Backup Created:",
                filename
            )


        except Exception as e:

            print(
                "Backup history error:",
                e
            )


        finally:

            db.close()


    # ---------------------------------------
    # Backup All Files
    # ---------------------------------------

    def backup_all_files(self, folder):

        if not os.path.exists(folder):

            print(
                "Backup folder not found:",
                folder
            )

            return


        print(
            "Starting backup of:",
            folder
        )


        for root, dirs, files in os.walk(folder):

            for file in files:

                path = os.path.join(
                    root,
                    file
                )

                self.backup_file(path)


        print("✓ Backup process completed")
        

