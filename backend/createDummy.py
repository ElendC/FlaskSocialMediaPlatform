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

    # Create 20 users with username user1 to user20
    for i in range(1, 21):
        username = f"user{i}"
        password = generate_password_hash(username)
        user = User(username=username, password=password)
        users.append(user)
        db.session.add(user)

    db.session.commit()  # Commit here to ensure user IDs are generated

    # Create user info for each user
    for i, user in enumerate(users):
        if i < 14:  # Users from user1 to user14
            bio = 'This is a random bio.' if i < 14 else None
            user_info = UserInfo(
                user_id=user.id,
                work=random.choice(['Engineer', 'Doctor', 'Teacher', 'Artist', 'Lawyer']),
                education=random.choice(['none', 'highschool', 'bachelor', 'master', 'phd']),
                hobbies=random.choice(['Reading', 'Swimming', 'Running', 'Cooking', 'Traveling']),
                age=random.randint(20, 50),
                location=random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                bio=bio
            )
            user_infos.append(user_info)
            db.session.add(user_info)
        elif i >= 14:  # Users from user15 to user20
            user_info = UserInfo(
                user_id=user.id,
                work=random.choice(['Engineer', 'Doctor', 'Teacher', 'Artist', 'Lawyer']),
                education=random.choice(['none', 'highschool', 'bachelor', 'master', 'phd']),
                hobbies=random.choice(['Reading', 'Swimming', 'Running', 'Cooking', 'Traveling']),
                age=random.randint(20, 50),
                location=random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                bio=""
            )
            user_infos.append(user_info)
            db.session.add(user_info)

    db.session.commit()

    #User1 is friends with user2 to user15
    user1 = users[0]
    for friend in users[1:15]:
        friendship = Friend(user1_id=user1.id, user2_id=friend.id)
        db.session.add(friendship)

    #User2 has friend requests from user3 to user20
    user2 = users[1]
    for requester in users[2:]:
        friend_request = FriendRequest(sender_id=requester.id, receiver_id=user2.id)
        db.session.add(friend_request)

    db.session.commit()
    print("20 dummy users created")

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

        # Uncomment these lines to delete all users, user info, friendships, and friend requests
        # delete_all_users()
        # delete_all_user_info()
        # delete_all_friends()
        # delete_all_friend_requests()
