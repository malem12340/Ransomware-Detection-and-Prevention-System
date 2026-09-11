import os


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "Ransomware_Project_2026"
    )

    DB_HOST = os.environ.get("DB_HOST")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = int(os.environ.get("DB_PORT", "3306"))