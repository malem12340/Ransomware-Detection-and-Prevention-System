import os
from urllib.parse import urlparse, unquote


class Config:

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "Ransomware_Project_2026"
    )

    # Railway MySQL on Render
    MYSQL_PUBLIC_URL = os.environ.get("MYSQL_PUBLIC_URL")

    if MYSQL_PUBLIC_URL:

        db_url = urlparse(MYSQL_PUBLIC_URL)

        DB_HOST = db_url.hostname
        DB_PORT = db_url.port
        DB_USER = unquote(db_url.username)
        DB_PASSWORD = unquote(db_url.password)
        DB_NAME = db_url.path.lstrip("/")

    else:
        # Local XAMPP MySQL
        DB_HOST = "localhost"
        DB_PORT = 3306
        DB_USER = "root"
        DB_PASSWORD = ""
        DB_NAME = "ransomware2_db"