import os
from urllib.parse import urlparse


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "Ransomware_Project_2026"
    )

    DB_URL = os.environ.get("MYSQL_PUBLIC_URL")

    if DB_URL:
        db_url = urlparse(DB_URL)

        DB_HOST = db_url.hostname
        DB_PORT = db_url.port
        DB_USER = db_url.username
        DB_PASSWORD = db_url.password
        DB_NAME = db_url.path.lstrip("/")
    else:
        DB_HOST = "localhost"
        DB_PORT = 3306
        DB_USER = "root"
        DB_PASSWORD = ""
        DB_NAME = "ransomware2_db"