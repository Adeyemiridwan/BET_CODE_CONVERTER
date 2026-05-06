from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    # PROFILE
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)

    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True)

    password_hash = db.Column(db.String(200), nullable=False)

    # VERIFICATION SYSTEM (ONE SYSTEM ONLY)
    verification_code = db.Column(db.String(10))
    verification_type = db.Column(db.String(20))  # email / phone / reset

    is_email_verified = db.Column(db.Boolean, default=False)
    is_phone_verified = db.Column(db.Boolean, default=False)

    # PROFILE
    profile_image = db.Column(db.String(255))

    # STATUS
    is_active = db.Column(db.Boolean, default=True)

    # RELATION
    wallet = db.relationship("Wallet", backref="user", uselist=False)
    
    # AUTHENTICATION
    session_token = db.Column(db.String(255), nullable=True)

    # PASSWORD METHODS
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    # TIMESTAMP
    created_at = db.Column(db.DateTime, server_default=db.func.now())