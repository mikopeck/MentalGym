from datetime import datetime, timedelta, timezone
from itsdangerous import URLSafeSerializer as Serializer
from flask import current_app
import hashlib

from database.models import db, User, IPTracking

# Rate limiting parameters
DAILY_LIMITS = {
    'free': 25,
    'paid': 250,
    'pro': 2500,
}

def reset_daily_limits(user):
    now = datetime.now(timezone.utc)
    if user.last_request_time.date() < now.date():
        user.daily_request_count = 0
        db.session.commit()

def increment_request_count(user):
    now = datetime.now(timezone.utc)
    user.daily_request_count += 1
    user.last_request_time = now
    db.session.commit()

def is_within_limit(user):
    now = datetime.now(timezone.utc)
    midnight = now + timedelta(days=1)
    midnight = midnight.replace(hour=0, minute=0, second=0, microsecond=0)
    time_until_reset = midnight - now

    reset_daily_limits(user)
    
    daily_limit = DAILY_LIMITS.get(user.tier, DAILY_LIMITS['free'])
    if user.daily_request_count >= daily_limit:
        hours, remainder = divmod(int(time_until_reset.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)
        message = f"Daily limit ({daily_limit}) exceeded. Please <a href='/plan' target='_blank'>upgrade your plan</a> or wait {hours} hours and {minutes} minutes before you send another message."
        return False, message

    if user.last_request_time:
        if isinstance(user.last_request_time, datetime) and user.last_request_time.tzinfo is None:
            user.last_request_time = user.last_request_time.replace(tzinfo=timezone.utc)

    if user.last_request_time and (now - user.last_request_time) <= timedelta(seconds=2):
        return False, "Cooldown triggered. Please wait a few seconds and try again."

    increment_request_count(user)
    return True, ""

def get_daily_request_count(user_id):
    user = User.query.get(user_id)
    return user.daily_request_count if user else 0


def set_user_tier(user_id, tier):
    user = User.query.get(user_id)
    if user:
        user.tier = tier
        db.session.commit()

def get_user_tier(user_id):
    user = User.query.get(user_id)
    return user.tier if user else None

def increment_violations(user_id):
    user = User.query.get(user_id)
    if user:
        user.violation_count += 1
        db.session.commit()

def generate_confirmation_token(user_id):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'confirm': str(user_id)})

def confirm(user_id, token):
    user = User.query.get(user_id)
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return False
    if str(data.get('confirm')) != str(user_id):
        return False
    user.confirmed = True
    user.confirmation_token = None
    db.session.commit()
    return True

def check_generation_allowed(ip, type):
    hashed_ip = hashlib.sha256(ip.encode()).hexdigest()
    record = IPTracking.query.filter_by(hashed_ip=hashed_ip).first()
    if record:
        if type == 'library' and record.library_generated:
            return False
        elif type == 'room' and record.room_generated:
            return False
    return True

def mark_generation_done(ip, type):
    hashed_ip = hashlib.sha256(ip.encode()).hexdigest()
    record = IPTracking.query.filter_by(hashed_ip=hashed_ip).first()
    if not record:
        record = IPTracking(ip)
        db.session.add(record)

    if type == 'library':
        record.library_generated = True
    elif type == 'room':
        record.room_generated = True

    db.session.commit()
