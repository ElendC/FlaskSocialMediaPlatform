import random
from flask import Flask
from models import db, User, UserInfo, Friend, FriendRequest
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_dummy_users():
    users = []
    user_infos = []

    for i in range(10):
        username = chr(97 + i)  # generates 'a', 'b', ..., 'j'
        password = generate_password_hash(username)
        user = User(username=username, password=password)
        users.append(user)
        db.session.add(user)

    db.session.commit()  # Commit here to ensure user IDs are generated

    for i in range(5):  # Only for the first 5 users
        user_info = UserInfo(
            user_id=users[i].id,
            work=random.choice(['Engineer', 'Doctor', 'Teacher', 'Artist', 'Lawyer']),
            education=random.choice(['High School', 'Bachelor', 'Master', 'PhD']),
            hobbies=random.choice(['Reading', 'Swimming', 'Running', 'Cooking', 'Traveling']),
            age=random.randint(20, 50),
            location=random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
            bio='This is a random bio.'
        )
        user_infos.append(user_info)
        db.session.add(user_info)

    db.session.commit()

    print("10 dummy users created, with random user info for the first 5 users")

def delete_all_users():
    User.query.delete()
    db.session.commit()
    print("All users deleted")

def delete_all_user_info():
    UserInfo.query.delete()
    db.session.commit()
    print("All user info deleted")

def delete_all_friends():
    Friend.query.delete()
    db.session.commit()
    print("All friendships deleted")

def delete_all_friend_requests():
    FriendRequest.query.delete()
    db.session.commit()
    print("All friend requests deleted")

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
        create_dummy_users()

        # delete_all_users()
        # delete_all_user_info()
        # delete_all_friends()
        # delete_all_friend_requests()
