from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    system_role = db.Column(db.String(100), default="PsychoAnalysis")
    profile = db.Column(db.Text, nullable=True)
    actions = db.Column(db.String(5000), default='')
    achievements = db.Column(db.String(5000), default='')
    ai_tutor_profile = db.Column(db.Text, nullable=True)
    current_lesson = db.Column(db.String(500), nullable=True)
    
    chats = db.relationship('ChatHistory', backref='user')
    completed_lessons = db.relationship('CompletedLesson', backref='user')
    completed_challenges = db.relationship('CompletedChallenge', backref='user')

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class CompletedLesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_name = db.Column(db.String(100), nullable=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)

class CompletedChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_name = db.Column(db.String(100), nullable=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)