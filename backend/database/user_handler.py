from datetime import datetime, timedelta
from itsdangerous import URLSafeSerializer as Serializer
from flask import current_app

from database.models import db, User

# Rate limiting parameters
DAILY_LIMITS = {
    'free': 20,
    'paid': 200,
    'pro': 2000,
}

def is_within_limit(user):
    now = datetime.utcnow()
    midnight = now + timedelta(days=1)
    midnight = midnight.replace(hour=0, minute=0, second=0, microsecond=0)
    time_until_reset = midnight - now

    if user.last_request_time.date() < now.date():
        user.daily_request_count = 0
    
    daily_limit = DAILY_LIMITS.get(user.tier, DAILY_LIMITS['free'])
    if user.daily_request_count >= daily_limit:
        hours, remainder = divmod(int(time_until_reset.total_seconds()), 3600)
        minutes = divmod(remainder, 60)
        return False, f"Daily limit ({daily_limit}) exceeded. Please wait {hours} hours and {minutes} minutes before you send another message."

    if user.last_request_time and (now - user.last_request_time) <= timedelta(seconds=2):
        return False, f"Cooldown triggered. Please wait a few seconds and try again."
    
    user.daily_request_count += 1
    print(f"Requests: {user.daily_request_count}")
    user.last_request_time = now
    db.session.commit()

    return True, ""

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