import os
import shutil
from db import Database


class BackupManager:

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

    def backup_file(self, file_path):

        if not os.path.exists(file_path):
            return

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            return

        os.makedirs(self.BACKUP_FOLDER, exist_ok=True)

        filename = os.path.basename(file_path)

        destination = os.path.join(

            self.BACKUP_FOLDER,

            filename

        )

        shutil.copy2(file_path, destination)

        db = Database()

        query = """

        INSERT INTO backup_history

        (file_name,original_path,backup_path)

        VALUES(%s,%s,%s)

        """

        values = (

            filename,

            file_path,

            destination

        )

        db.execute(query, values)

        db.close()

        print("Backup Created :", filename)


    def backup_all_files(self, folder):

        if not os.path.exists(folder):
            return

        for root, dirs, files in os.walk(folder):

            for file in files:

                path = os.path.join(root, file)

                self.backup_file(path)