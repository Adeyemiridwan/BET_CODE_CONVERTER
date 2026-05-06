from app.extensions import db
from datetime import datetime


class Conversion(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    input_code = db.Column(db.String(200), nullable=False)

    output_code = db.Column(db.String(200), nullable=False)

    fee_charged = db.Column(db.Float, default=0)

    created_at = db.Column(db.DateTime, default=db.func.now())