# routes/auth_routes.py
from datetime import datetime
from flask import request, jsonify, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError
import pymysql.err as pymysql_err
from oauth2client import client, crypt

from database.models import db, User
from database.user_handler import confirm, generate_confirmation_token
from message_handler import initialize_messages
from email_provider.resend_api import send_registration_email
from email_provider.email_templates import Registration

GOOGLE_CLIENT_ID = "529262341360-9sq10od3qkro19jaavhgachkpviugfv3.apps.googleusercontent.com"

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

    @app.route("/logout", methods=["GET"])
    @login_required
    def logout_route():
        logout_user()
        return jsonify({"status": "success"})

    @app.route('/check-auth', methods=['GET'])
    def check_auth():
        return jsonify({'loggedIn': current_user.is_authenticated})

    @app.route('/signup', methods=['POST'])
    def signup():
        try:
            email = request.form['new-email']
            password = request.form['new-password']
            hashed_password = generate_password_hash(password)
            new_user = User(email=email, password=hashed_password, username=email)
            db.session.add(new_user)
            db.session.commit()
            new_user.confirmation_token = generate_confirmation_token(new_user.id)
            new_user.confirm_sent_at = datetime.utcnow()
            db.session.commit()
            
            confirmation_link = url_for('confirm_email', token=new_user.confirmation_token, _external=True)
            send_registration_email(email, Registration, confirmation_link)
            return jsonify({'status': 'success'})
        except IntegrityError as e:
            if isinstance(e.orig, pymysql_err.IntegrityError) and 'Duplicate entry' in str(e.orig):
                return jsonify({'status': 'error', 'message': 'An account with this email already exists.'}), 400
            else:
                return jsonify({'status': 'error', 'message': 'An unexpected error occurred. Please try again later.'}), 500

    @app.route('/confirm/<token>')
    def confirm_email(token):
        user = User.query.filter_by(confirmation_token=token).first()
        if user and confirm(user.id, token):
            login_user(user)
            initialize_messages(user.id)
            return redirect('/?awake')
        else:
            if user is not None and not user.confirmed:
                user.confirmation_token = generate_confirmation_token(user.id)
                user.confirm_sent_at = datetime.utcnow()
                db.session.commit()
                
                # Send a new confirmation email
                confirmation_link = url_for('confirm_email', token=user.confirmation_token, _external=True)
                send_registration_email(user.email, Registration, confirmation_link)
                return redirect('/about?message=expired_registration_token')
            return redirect('/about?message=invalid_registration_token')
    
    @app.route('/auth/google/callback', methods=['POST'])
    def google_auth_callback():
        token = request.json.get('id_token')

        try:
            idinfo = client.verify_id_token(token, GOOGLE_CLIENT_ID)

            if idinfo['aud'] not in [GOOGLE_CLIENT_ID]:
                raise crypt.AppIdentityError("Unrecognized client.")

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")
            
            userid = idinfo['sub']
            email = idinfo.get('email')
            name = idinfo.get('name')
            # picture = idinfo.get('picture')
            
            if not idinfo.get('email_verified'):
                raise ValueError('Email not verified by Google.')

        except crypt.AppIdentityError:
            return jsonify({'message': 'Invalid token'}), 401

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                username=name,
                confirmed=True,
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return jsonify({'status': "success", "message":"new_user"}), 200
        else:
            user.username = name
            user.confirmed = True
            db.session.commit()
            login_user(user)
            return jsonify({'status': "success", "message":"existing_user"}), 200

