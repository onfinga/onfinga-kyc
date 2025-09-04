from flask import Blueprint, request, jsonify
from app.models import db, User


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
data = request.json
if User.query.filter_by(email=data['email']).first():
return jsonify({"message": "User already exists."}), 400
user = User(email=data['email'])
db.session.add(user)
db.session.commit()
return jsonify({"message": "User registered successfully."}), 201