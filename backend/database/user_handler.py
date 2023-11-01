from datetime import datetime, timedelta

from database.models import db

# Rate limiting parameters
DAILY_LIMITS = {
    'free': 10,
    'paid': 100,
    'pro': 1000,
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

    if user.last_request_time and (now - user.last_request_time) <= timedelta(seconds=20):
        return False, f"Request limit exceeded. Please take some time to think before you send another message."
    
    user.daily_request_count += 1
    user.last_request_time = now
    db.session.commit()

    return True, ""