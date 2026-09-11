import os


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "Ransomware_Project_2026"
    )

    DB_HOST = os.environ.get("DBHOST", "localhost")
    DB_PORT = int(os.environ.get("DBPORT", "3306"))
    DB_USER = os.environ.get("DBUSER", "root")
    DB_PASSWORD = os.environ.get("DBPASSWORD", "")
    DB_NAME = os.environ.get("DBNAME", "ransomware2_db")