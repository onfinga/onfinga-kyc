from flask import Blueprint, request, jsonify
from app.models import db, KYCSubmission


kyc_bp = Blueprint('kyc', __name__)


@kyc_bp.route('/submit', methods=['POST'])
def submit_kyc():
data = request.json
kyc = KYCSubmission(
user_id=data['user_id'],
id_number=data['id_number'],
income_verified=False
)
db.session.add(kyc)
db.session.commit()
return jsonify({"message": "KYC submission received."}), 201