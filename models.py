# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # 'pending' or 'completed'

    def __repr__(self):
        return f'<Task {self.title}>'
