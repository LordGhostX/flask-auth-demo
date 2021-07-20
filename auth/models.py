from datetime import datetime
from auth import db


class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True, nullable=False)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
