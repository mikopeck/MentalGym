# routes/auth_routes.py

from flask import request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
import pymysql.err as pymysql_err

from ..models import db, User
from ..message_handler import initialize_messages

def init_auth_routes(app):

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
    
    @LoginManager.unauthorized_handler
    def unauthorized():
        return make_response(jsonify({"error": "User not authenticated"}), 401)
