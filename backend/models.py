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
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #To check friendship both ways
    @staticmethod
    def is_friends(user1_id, user2_id):
        return Friend.query.filter(
            ((Friend.user1_id == user1_id) & (Friend.user2_id == user2_id)) |
            ((Friend.user1_id == user2_id) & (Friend.user2_id == user1_id))
        ).first() is not None

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserInfo(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True, nullable=False)
    work = db.Column(db.String(50), nullable=True)
    education = db.Column(db.String(50), nullable=True)
    hobbies = db.Column(db.String(200), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    bio = db.Column(db.Text, nullable=True)