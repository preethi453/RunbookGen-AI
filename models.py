from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RunbookHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    mode = db.Column(db.String(100), default="Unknown")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)