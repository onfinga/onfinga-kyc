import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root explicitly (two levels up from this file)
ROOT = Path(__file__).resolve().parents[2]  # .../onfinga-kyc
load_dotenv(ROOT / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
