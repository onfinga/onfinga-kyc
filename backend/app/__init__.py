from dotenv import load_dotenv
load_dotenv()  # load .env before reading Config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os

from backend.app.config import Config
from backend.app.routes import main

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Runtime sanity checks (helpful in prod)
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY is missing")
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        raise RuntimeError("DATABASE_URL is missing")

    db.init_app(app)
    migrate.init_app(app, db)

    # Restrict CORS to your frontend
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    CORS(
        app,
        resources={r"/*": {"origins": [frontend_origin]}},
        supports_credentials=False,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        max_age=3600,
    )

    # Admin panel (optional; guarded so missing deps won't crash app)
    from backend.app.models import KYCSession
    try:
        from flask_admin import Admin
        from backend.app.admin import SecureModelView
        admin = Admin(app, name="Onfinga Admin", template_mode="bootstrap4")
        admin.add_view(SecureModelView(KYCSession, db.session))
    except Exception as e:
        # You can log this if you like:
        # app.logger.warning(f"Admin panel not initialized: {e}")
        pass

    app.register_blueprint(main)
    return app
