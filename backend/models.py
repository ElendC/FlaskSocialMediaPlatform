from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profileImg = db.Column(db.String(300))

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    friend1 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend2 = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(50), default='pending') 
