from app.extensions import db
from datetime import datetime


class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    type = db.Column(db.String(50))  # deposit, conversion_fee

    amount = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=db.func.now())