from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager

from auth import auth_bp
from models import db, User

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='') #Creates Flask Instance. Arguments is where static compiled frontend files are.
app.config['SECRET_KEY'] = 'someSecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)
db.init_app(app)

#flask login setup
lim = LoginManager()
lim.login_view = 'auth.login'
lim.init_app(app)

@lim.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)