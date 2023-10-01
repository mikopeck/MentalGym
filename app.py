#app.py

import os
import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_cors import CORS
from flask import send_from_directory
from sqlalchemy.exc import IntegrityError
import pymysql.err as pymysql_err

from system_guide import progress
from models import db, User
from message_handler import initialize_messages
import db_handlers as dbh

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
    
@app.route("/api/recent_messages", methods=["GET"])
@login_required
def get_recent_messages_route():
    return jsonify(messages=dbh.get_recent_messages(current_user.id), actions=dbh.get_actions(current_user.id))

@app.route("/api/messages", methods=["POST"])
@login_required
def post_message():
    userInput = request.form["message"]
    progress(current_user.id, userInput)
    return jsonify(messages=dbh.get_recent_messages(current_user.id), actions=dbh.get_actions(current_user.id))

@app.route("/api/profile", methods=["GET"])
@login_required
def get_profile_route():
    profile_data = {
        "user": dbh.get_profile(current_user.id),
        "tutor": dbh.get_tutor(current_user.id)
    }
    return jsonify(status="success", profile=profile_data)

@app.route("/api/profile/user", methods=["POST"])
@login_required
def update_user_profile():
    new_data = request.json.get("data")
    dbh.set_profile(current_user.id, new_data)
    return jsonify(status="success")

@app.route("/api/profile/tutor", methods=["POST"])
@login_required
def update_tutor_profile():
    new_data = request.json.get("data")
    dbh.set_tutor(current_user.id, new_data)
    return jsonify(status="success")

@app.route("/api/challenges", methods=["GET"])
@login_required
def get_challenges_route():
    challenges_data = {
        "active": dbh.get_active_challenges(current_user.id),
        "completed": dbh.get_completed_challenges(current_user.id)
    }
    return jsonify(status="success", challenges=challenges_data)

@app.route("/api/achievements", methods=["GET"])
@login_required
def get_achievements_route():
    achievements_data = dbh.get_user_achievements(current_user.id)
    return jsonify(status="success", achievements=achievements_data)

@app.route("/reset", methods=["GET"])
@login_required
def reset():
    dbh.reset_user_profile(current_user.id)
    initialize_messages(current_user.id)
    return jsonify(messages=dbh.get_recent_messages(current_user.id), actions=[], status="success")

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
    try:
        email = request.form['new-email']
        password = request.form['new-password']
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password, username=email)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        initialize_messages(current_user.id)
        return jsonify({'status': 'success'})
    except IntegrityError as e:
        if isinstance(e.orig, pymysql_err.IntegrityError) and 'Duplicate entry' in str(e.orig):
            return jsonify({'status': 'error', 'message': 'An account with this email already exists.'}), 400
        else:
            return jsonify({'status': 'error', 'message': 'An unexpected error occurred. Please try again later.'}), 500

@app.route("/logout", methods=["GET"])
@login_required
def logout_route():
    logout_user()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)