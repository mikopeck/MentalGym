#app.py

import os
import openai
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_cors import CORS
from flask import send_from_directory

from system_guide import progress
from models import db, User
from db_handlers import get_recent_messages, get_actions, clear_chat_history
from message_handler import initialize_messages

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
openai.api_key = os.getenv("OPENAI_API_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    session = db.session
    return session.get(User, int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://root:password@localhost/mind_forge_ai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists("mental-gym/dist/" + path):
        return send_from_directory('mental-gym/dist', path)
    else:
        return send_from_directory('mental-gym/dist', 'index.html')

@app.route("/api/messages", methods=["POST"])
@login_required
def post_message():
    userInput = request.form["message"]
    progress(current_user.id, userInput)
    return jsonify(messages=get_recent_messages(current_user.id), actions=get_actions(current_user.id))

@app.route("/reset", methods=["GET"])
@login_required
def reset():
    clear_chat_history(current_user.id)
    initialize_messages(current_user.id)
    return jsonify({"status": "success"})

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['new-email']
    password = request.form['new-password']
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, username=email)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    initialize_messages(current_user.id)
    return jsonify({'status': 'success'})

@app.route("/logout", methods=["GET"])
@login_required
def logout_route():
    logout_user()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)