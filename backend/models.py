from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    system_role = db.Column(db.String(100), default='')
    profile = db.Column(db.Text, nullable=True)
    ai_tutor_profile = db.Column(db.Text, nullable=True)
    current_lesson = db.Column(db.String(500), nullable=True)
    
    achievements = db.relationship('UserAchievement', backref='user')
    actions = db.relationship('UserAction', backref='user')

    chats = db.relationship('ChatHistory', backref='user')
    challenges = db.relationship('Challenge', backref='user')
    lessons = db.relationship('Lesson', backref='user')

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow)

class UserAction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    system_role = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_name = db.Column(db.String(100), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_name = db.Column(db.String(100), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    system_role = db.Column(db.String(100), default='')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
