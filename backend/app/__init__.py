from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from backend.app.config import Config
from backend.app.routes import main
from backend.app.admin import SecureModelView  # if you have this

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # ✅ Restrict CORS to a single origin (frontend)
    frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    CORS(
        app,
        resources={r"/*": {"origins": [frontend_origin]}},
        supports_credentials=False,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        max_age=3600,
    )

    # Admin / blueprints
    from backend.app.models import KYCSession
    try:
        from flask_admin import Admin
        from backend.app.admin import SecureModelView
        admin = Admin(app, name="Onfinga Admin", template_mode="bootstrap4")
        admin.add_view(SecureModelView(KYCSession, db.session))
    except Exception:
        pass

    app.register_blueprint(main)
    return app
