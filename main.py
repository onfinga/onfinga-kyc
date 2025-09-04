from backend.app import create_app, db
from backend.app.models import KYCSession
from backend.app.routes import main  # 👈 Add this to force blueprint to load

from flask import url_for

app = create_app()

# DEBUG: Print registered routes
with app.app_context():
    print("\n📦 Registered Routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

if __name__ == "__main__":
    app.run(debug=True)
