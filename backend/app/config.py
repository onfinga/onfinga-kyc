import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://malcolmsolomon@localhost:5432/onfinga_kyc_dev"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False