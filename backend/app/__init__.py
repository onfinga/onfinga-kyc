from flask_admin import Admin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables

from backend.app.routes import main
from backend.app.config import Config
from backend.app.admin import SecureModelView  # ✅ Custom secured view

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # ✅ Admin panel setup with SecureModelView
    from backend.app.models import KYCSession
    admin = Admin(app, name="Onfinga Admin", template_mode="bootstrap4")
    admin.add_view(SecureModelView(KYCSession, db.session))  # ✅ Secure version
    print("✅ Admin panel registered at /admin/")

    app.register_blueprint(main)

    return app