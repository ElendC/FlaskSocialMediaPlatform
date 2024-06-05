from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_required
from werkzeug.utils import secure_filename
import os

from auth import auth_bp
from models import db, User

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='') # Creates Flask Instance. Arguments is where static compiled frontend files are.
app.config['SECRET_KEY'] = 'someSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../frontend/src/store/uploads') # For flask image upload

CORS(app, supports_credentials=True)
db.init_app(app)

# flask login setup
lim = LoginManager()
lim.login_view = 'auth.login'
lim.init_app(app)

@lim.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# flask login setup

app.register_blueprint(auth_bp)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Uploading profile picture
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'photo' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['photo']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        #Forcing name
        unique_filename = f"user_{current_user.id}_profile.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        #Overwriting previous, to avoid many uploads
        file.save(filepath)
        
        # Update profile pic in db
        user = User.query.get(current_user.id)
        user.profileImg = unique_filename
        db.session.commit()
        
        return jsonify({'filename': unique_filename}), 200
    
    return jsonify({'message': 'File upload failed'}), 500

@app.route('/store/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database and tables
    app.run(debug=True)


