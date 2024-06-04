from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User

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

##REMOVE maybe##
@auth_bp.route('/api/user/<int:id>', methods=['GET'])
@login_required
def get_user_by_id(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({
        'id': user.id,
        'username': user.username,
        'profileImg': user.profileImg
    })

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
