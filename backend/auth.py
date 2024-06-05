from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, FriendRequest, Friend

from flask import current_app as app #For debug/loging: app.logger.info(f"Message: {variable}")

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Username already in use'}), 400
    
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    login_user(user)

    return jsonify({'message': 'Registered successfully'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401
    
    login_user(user)
    app.logger.info(f"Logged in as user: {user}")


    return jsonify({'message': 'Login successful'})

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@auth_bp.route('/status', methods=['GET'])
def status():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True})
    return jsonify({'logged_in': False})

@auth_bp.route('/current_user', methods=['GET'])
@login_required
def current_user_view():
    return jsonify({'username': current_user.username})


@auth_bp.route('/api/user/username/<username>', methods=['GET'])
@login_required
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'profileImg': user.profileImg
    })


#FRIEND REQUEST STUFF
@auth_bp.route('/api/friend_request/send', methods=['POST'])
@login_required
def send_friend_request():
    data = request.get_json()
    receiver_username = data.get('receiver_username')
    receiver = User.query.filter_by(username=receiver_username).first()

    if not receiver:
        app.logger.info("No receiver")
        return jsonify({'message': 'User not found'}), 404
    if receiver.id == current_user.id:
        app.logger.info("You can't befriend yourself...")
        return jsonify({'message': 'Try to find some other friends, not yourself'}), 400

    alreadySent = FriendRequest.query.filter_by(sender_id=current_user.id, receiver_id=receiver.id).first()
    if alreadySent:
        app.logger.info("Friend request already sent")
        return jsonify({'message': 'Wait patiently for a response'}), 400

    #Check if already friends both ways
    if Friend.is_friends(current_user.id, receiver.id):
        return jsonify({'message': 'You are already friends'}), 400

    bothRequesting = FriendRequest.query.filter_by(sender_id=receiver.id, receiver_id=current_user.id).first()
    if bothRequesting:
        friendship = Friend(user1_id=current_user.id, user2_id=receiver.id)
        db.session.add(friendship)

        # Remove the reciprocal friend request
        db.session.delete(bothRequesting)
        db.session.commit()
        return jsonify({'message': 'You are now friends!'}), 200

    #Create a new friend request
    friend_request = FriendRequest(sender_id=current_user.id, receiver_id=receiver.id)
    db.session.add(friend_request)
    db.session.commit()
    app.logger.info(f"sender is: {current_user}")
    app.logger.info(f"receiver is: {receiver}")
    return jsonify({'message': 'Friend request sent'}), 200


@auth_bp.route('/api/friend_request/respond', methods=['POST'])
@login_required
def respond_friend_request():
    data = request.get_json()
    request_id = data.get('request_id')
    action = data.get('action')  # 'accept' or 'decline'

    friend_request = FriendRequest.query.get(request_id)
    if not friend_request:
        return jsonify({'message': 'Friend request not found'}), 404
    if friend_request.receiver_id != current_user.id:
        return jsonify({'message': 'This is not for you, get your own friends'}), 403
    if action == 'accept':
        #Check if friends
        if not Friend.is_friends(current_user.id, friend_request.sender_id):
            friendship = Friend(user1_id=current_user.id, user2_id=friend_request.sender_id)
            db.session.add(friendship)

        db.session.delete(friend_request)
        db.session.commit()
        return jsonify({'message': 'Friend request accepted'}), 200
    
    elif action == 'decline':
        db.session.delete(friend_request)
        db.session.commit()
        return jsonify({'message': 'Friend request declined'}), 200
    else:
        return jsonify({'message': 'Invalid action'}), 400

    
@auth_bp.route('/api/friends', methods=['GET'])
@login_required
def get_friends():
    friends = Friend.query.filter((Friend.user1_id == current_user.id) | (Friend.user2_id == current_user.id)).all()
    friend_list = []
    for friend in friends:
        if friend.user1_id == current_user.id:
            friend_user = User.query.get(friend.user2_id)
        else:
            friend_user = User.query.get(friend.user1_id)
        friend_list.append({'id': friend_user.id, 'username': friend_user.username, 'profileImg': friend_user.profileImg})
    return jsonify(friend_list), 200


@auth_bp.route('/api/friend_requests', methods=['GET'])
@login_required
def get_friend_requests():
    received_requests = FriendRequest.query.filter_by(receiver_id=current_user.id).all()
    sent_requests = FriendRequest.query.filter_by(sender_id=current_user.id).all()
    received_requests_list = [{'id': req.id, 'sender_username': User.query.get(req.sender_id).username} for req in received_requests]
    sent_requests_list = [{'id': req.id, 'receiver_username': User.query.get(req.receiver_id).username} for req in sent_requests]
    app.logger.info(f"Friend requests sent: {sent_requests_list}")
    app.logger.info(f"Friend requests received: {received_requests_list}")
    return jsonify({'received_requests': received_requests_list, 'sent_requests': sent_requests_list}), 200
