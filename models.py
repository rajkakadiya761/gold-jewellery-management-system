# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_confirmed = db.Column(db.Integer, default=0)  # Add confirmation status

    def __repr__(self):
        return f"<User {self.name}, {self.email}>"
    
class Complaints(db.Model):
    complaint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pending', 'inprocess', 'resolved'), default='pending')
    type = db.Column(db.Enum('delivery', 'product', 'packaging'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


