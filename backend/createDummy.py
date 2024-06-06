import random
from flask import Flask
from models import db, User, UserInfo, Friend
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_dummy_users():
    users = []

    # Create users with usernames 1 to 10
    for i in range(1, 11):
        username = str(i)
        password = generate_password_hash(username)
        user = User(username=username, password=password)
        users.append(user)
        db.session.add(user)
    
    # Create users with usernames a, s, d, f, g, h, j, k, l
    for username in ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l']:
        password = generate_password_hash(username)
        user = User(username=username, password=password)
        users.append(user)
        db.session.add(user)
    
    db.session.commit()  # Commit here to ensure user IDs are generated

    # Create UserInfo with default values for each user
    for user in users:
        user_info = UserInfo(
            user_id=user.id,
            work='Engineer',
            education='Bachelor',
            hobbies='Reading',
            age=30,
            location='New York',
            bio='This is a default bio.'
        )
        db.session.add(user_info)
    
    db.session.commit()

    # Create friendships
    user_dict = {user.username: user.id for user in users}
    
    # User '1' is friends with everyone
    user_one_id = user_dict['1']
    for username, user_id in user_dict.items():
        if user_id != user_one_id:
            friendship = Friend(user1_id=user_one_id, user2_id=user_id)
            db.session.add(friendship)
    
    # Create random friendships for the rest
    remaining_users = [user_id for username, user_id in user_dict.items() if user_id != user_one_id]
    for user_id in remaining_users:
        friends = random.sample(remaining_users, k=random.randint(1, 5))
        for friend_id in friends:
            if user_id != friend_id:
                # Ensure the friendship is added only once
                if not Friend.query.filter(
                    ((Friend.user1_id == user_id) & (Friend.user2_id == friend_id)) |
                    ((Friend.user1_id == friend_id) & (Friend.user2_id == user_id))
                ).first():
                    friendship = Friend(user1_id=user_id, user2_id=friend_id)
                    db.session.add(friendship)

    db.session.commit()
    print("Dummy users, user info, and friendships created")

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

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        delete_all_users()        # Clear previous data
        delete_all_user_info()    # Clear previous data
        delete_all_friends()      # Clear previous data
        create_dummy_users()

        # Uncomment to delete
        # delete_all_users()
        # delete_all_user_info()
        # delete_all_friends()
