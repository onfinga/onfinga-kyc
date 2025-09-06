import os


class Config:
    # Require SECRET_KEY
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("❌ SECRET_KEY is not set in environment variables!")

    # Require DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("❌ DATABASE_URL is not set in environment variables!")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
