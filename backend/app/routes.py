print("✅ Loaded backend/app/routes.py")
from flask import Blueprint, request, jsonify
import uuid
import re
from datetime import datetime

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return jsonify({"message": "Onfinga KYC backend is running."})

@main.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True}), 200

@main.route("/kyc/start", methods=["POST"])
def start_kyc():
    from backend.app.models import KYCSession, User
    from backend.app import db
    try:
        print("🔥 /kyc/start endpoint hit")
        data = request.get_json() or {}
        print("🧾 Received data:", data)

        email = data.get("email")
        if not email or not EMAIL_RE.match(email):
            return jsonify({"error": "Invalid or missing email.", "code": "invalid_email"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": f"User with email '{email}' not found.", "code": "user_not_found"}), 404

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
        return jsonify({"error": str(e), "code": "internal_server_error"}), 500

@main.route("/kyc/status/<session_id>", methods=["GET"])
def get_kyc_status(session_id):
    from backend.app.models import KYCSession
    print(f"🔍 Checking status for session: {session_id}")
    session = KYCSession.query.filter_by(session_id=session_id).first()
    if not session:
        return jsonify({"error": f"Session '{session_id}' not found.", "code": "session_not_found"}), 404
    return jsonify({"session_id": session.session_id, "status": session.status}), 200

@main.route("/kyc/update/<session_id>", methods=["POST"])
def update_kyc_status(session_id):
    from backend.app.models import KYCSession
    from backend.app import db
    try:
        data = request.get_json() or {}
        new_status = data.get("status")
        if new_status not in ["approved", "rejected"]:
            return jsonify({"error": "Invalid status. Must be 'approved' or 'rejected'.", "code": "invalid_status"}), 400

        session = KYCSession.query.filter_by(session_id=session_id).first()
        if not session:
            return jsonify({"error": f"Session '{session_id}' not found.", "code": "session_not_found"}), 404

        session.status = new_status
        session.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "session_id": session.session_id,
            "new_status": session.status,
            "message": f"Session updated to '{new_status}'"
        }), 200

    except Exception as e:
        print("❌ Error in /kyc/update:", str(e))
        return jsonify({"error": str(e), "code": "internal_server_error"}), 500

@main.route("/kyc/list", methods=["GET"])
def list_kyc_sessions():
    from backend.app.models import KYCSession, User
    email = request.args.get("email")
    user_id_param = request.args.get("user_id")

    # Resolve to a numeric user_id
    resolved_user_id = None
    if email:
        if not EMAIL_RE.match(email):
            return jsonify({"error": "Invalid email.", "code": "invalid_email"}), 400
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "User not found.", "code": "user_not_found"}), 404
        resolved_user_id = user.id
    elif user_id_param:
        try:
            resolved_user_id = int(user_id_param)
        except ValueError:
            return jsonify({"error": "user_id must be an integer.", "code": "invalid_user_id"}), 400
    else:
        return jsonify({"error": "Provide either 'email' or 'user_id' query param.", "code": "missing_identifier"}), 400

    sessions = KYCSession.query.filter_by(user_id=resolved_user_id).order_by(KYCSession.created_at.desc()).all()
    return jsonify({
        "user_id": resolved_user_id,
        "sessions": [{
            "session_id": s.session_id,
            "status": s.status,
            "created_at": (s.created_at.isoformat() if s.created_at else None),
            "updated_at": (s.updated_at.isoformat() if s.updated_at else None)
        } for s in sessions]
    }), 200
