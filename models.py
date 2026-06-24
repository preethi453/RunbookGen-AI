from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RunbookHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.Text)
    result = db.Column(db.Text)
    mode = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))
