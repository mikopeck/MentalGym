from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    
    system_role = db.Column(db.String(100), default='')
    profile = db.Column(db.Text, nullable=True)
    ai_tutor_profile = db.Column(db.Text, nullable=True)
    current_content = db.Column(db.String(500), nullable=True)
    
    achievements = db.relationship('UserAchievement', backref='user')
    actions = db.relationship('UserAction', backref='user')

    chats = db.relationship('ChatHistory', backref='user')
    challenges = db.relationship('Challenge', backref='user')
    lessons = db.relationship('Lesson', backref='user')

    tier = db.Column(db.String(50), default='free')  # 'free', 'paid', 'pro'
    daily_request_count = db.Column(db.Integer, default=0)
    last_request_time = db.Column(db.DateTime, default=datetime.utcnow)

    violation_count = db.Column(db.Integer, default=0)

    confirmed = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(100), nullable=True)
    confirm_sent_at = db.Column(db.DateTime, nullable=True)

    def as_dict(self):
        active_challenges = [challenge.challenge_name for challenge in sorted(
            [c for c in self.challenges if not c.completion_date], 
            key=lambda x: x.id, reverse=True)[:5]
        ]

        completed_challenges = [challenge.challenge_name for challenge in sorted(
            [c for c in self.challenges if c.completion_date], 
            key=lambda x: x.id, reverse=True)[:5]
        ]

        active_lessons = [lesson.lesson_name for lesson in sorted(
            [l for l in self.lessons if not l.completion_date], 
            key=lambda x: x.id, reverse=True)[:5]
        ]

        completed_lessons = [lesson.lesson_name for lesson in sorted(
            [l for l in self.lessons if l.completion_date], 
            key=lambda x: x.id, reverse=True)[:5]
        ]

        user_data = {
            "profile": self.profile,
            "active_challenges": active_challenges,
            "completed_challenges": completed_challenges,
            "active_lessons": active_lessons,
            "completed_lessons": completed_lessons,
            "latest_action": self.current_content
        }
        return user_data

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)

class UserAchievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    completion_date = db.Column(db.DateTime, default=datetime.utcnow())

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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)
    message_type = db.Column(db.String(50), default='message')
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # 1-5 scale
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    status = db.Column(db.String(50), default='new')  # e.g., new, reviewed, resolved

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=True)

    user = db.relationship('User', backref=db.backref('feedback', lazy=True))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_name = db.Column(db.String(100), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    shared = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_name = db.Column(db.String(100), nullable=False)
    completion_date = db.Column(db.DateTime, nullable=True)
    system_role = db.Column(db.String(100), default='')
    shared = db.Column(db.Boolean, default=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
