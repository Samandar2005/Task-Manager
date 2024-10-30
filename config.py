import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///tasks.db")  # SQLite uchun
    SQLALCHEMY_TRACK_MODIFICATIONS = False