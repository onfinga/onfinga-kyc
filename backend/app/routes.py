print("✅ Loaded backend/app/routes.py")
from flask import Blueprint, request, jsonify
import uuid
import re

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return jsonify({"message": "Onfinga KYC backend is running."})


@main.route("/kyc/start", methods=["POST"])
def start_kyc():
    from backend.app.models import KYCSession, User
    from backend.app import db
    from datetime import datetime

    try:
        print("🔥 /kyc/start endpoint hit")
        data = request.get_json()
        print("🧾 Received data:", data)

        email = data.get("email")
        if not email:
            return jsonify({
                "error": "Missing email.",
                "code": "missing_email"
            }), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                "error": f"User with email '{email}' not found.",
                "code": "user_not_found"
            }), 404

        session_id = f"kyc_{user.id}_{uuid.uuid4().hex[:8]}"
        print("🆔 Generated session_id:", session_id)

        kyc_session = KYCSession(
            session_id=session_id,
            user_id=user.id,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(kyc_session)
        db.session.commit()
        print("✅ KYC session committed to DB")

        return jsonify({
            "session_id": session_id,
            "status": "pending",
            "message": f"KYC session started for user_id {user.id}"
        }), 200

    except Exception as e:
        print("❌ Error in /kyc/start:", str(e))
        return jsonify({
            "error": str(e),
            "code": "internal_server_error"
        }), 500


@main.route("/kyc/status/<session_id>", methods=["GET"])
def get_kyc_status(session_id):
    from backend.app.models import KYCSession

    print(f"🔍 Checking status for session: {session_id}")
    session = KYCSession.query.filter_by(session_id=session_id).first()

    if not session:
        return jsonify({
            "error": f"Session '{session_id}' not found.",
            "code": "session_not_found"
        }), 404

    return jsonify({
        "session_id": session.session_id,
        "status": session.status
    }), 200


@main.route("/kyc/update/<session_id>", methods=["POST"])
def update_kyc_status(session_id):
    from backend.app.models import KYCSession
    from backend.app import db

    try:
        data = request.get_json()
        new_status = data.get("status")

        if new_status not in ["approved", "rejected"]:
            return jsonify({
                "error": "Invalid status. Must be 'approved' or 'rejected'.",
                "code": "invalid_status"
            }), 400

        session = KYCSession.query.filter_by(session_id=session_id).first()
        if not session:
            return jsonify({
                "error": f"Session '{session_id}' not found.",
                "code": "session_not_found"
            }), 404

        session.status = new_status
        db.session.commit()

        return jsonify({
            "session_id": session.session_id,
            "new_status": session.status,
            "message": f"Session updated to '{new_status}'"
        }), 200

    except Exception as e:
        print("❌ Error in /kyc/update:", str(e))
        return jsonify({
            "error": str(e),
            "code": "internal_server_error"
        }), 500


@main.route("/kyc/list", methods=["GET"])
def list_kyc_sessions():
    from backend.app.models import KYCSession

    user_id = request.args.get("user_id")
    if not user_id or not re.match(r"^[a-zA-Z0-9_]{3,30}$", user_id):
        return jsonify({
            "error": "Missing or invalid user_id.",
            "code": "invalid_user_id"
        }), 400

    sessions = KYCSession.query.filter_by(user_id=user_id).all()

    return jsonify({
        "sessions": [
            {
                "session_id": s.session_id,
                "status": s.status,
                "created_at": s.created_at.isoformat(),
                "updated_at": s.updated_at.isoformat()
            } for s in sessions
        ]
    }), 200
