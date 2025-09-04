from backend.app import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔗 One-to-many relationship: A user can have many KYC sessions
    kyc_sessions = db.relationship('KYCSession', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.id} - {self.email}>"


class KYCSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_number = db.Column(db.String(50), nullable=False)
    income_verified = db.Column(db.Boolean, default=False, nullable=False)
    document_path = db.Column(db.String(200), nullable=True)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<KYCSubmission user_id={self.user_id} verified={self.income_verified}>"


class KYCSession(db.Model):
    __tablename__ = 'kyc_sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<KYCSession {self.session_id} status={self.status}>"
