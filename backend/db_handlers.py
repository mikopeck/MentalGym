from models import db, User, ChatHistory, Challenge, Lesson, UserAction, Achievement, UserAchievement
from utils import decode_if_needed

history_limit = 16

def add_user_message(user_id, message_content, challenge_id=None, lesson_id=None):
    message = ChatHistory(
        user_id=user_id, 
        message=message_content, 
        role="user", 
        system_role="User",
        challenge_id=challenge_id,
        lesson_id=lesson_id
    )
    db.session.add(message)
    db.session.commit()

def add_ai_response(user_id, response, sys_role, challenge_id=None, lesson_id=None):
    ai_message = response['choices'][0]['message']['content']
    add_ai_message(user_id, ai_message, sys_role, challenge_id, lesson_id)

def add_ai_message(user_id, message_content, sys_role, challenge_id=None, lesson_id=None):
    message = ChatHistory(
        user_id=user_id, 
        message=decode_if_needed(message_content), 
        role="assistant", 
        system_role=sys_role,
        challenge_id=challenge_id,
        lesson_id=lesson_id
    )
    db.session.add(message)
    db.session.commit()

def get_recent_messages(user_id, lesson_id=None, challenge_id=None):
    query = ChatHistory.query.filter_by(user_id=user_id)
    if lesson_id is not None:
        query = query.filter_by(lesson_id=lesson_id)
    if challenge_id is not None:
        query = query.filter_by(challenge_id=challenge_id)
        
    recent_messages = query.order_by(ChatHistory.timestamp.desc()).limit(history_limit).all()
    recent_messages = recent_messages[::-1]
    return [{"role": msg.role, "content": msg.message, "system_role": msg.system_role} for msg in recent_messages]

def get_api_messages(user_id, lesson_id=None, challenge_id=None):
    query = ChatHistory.query.filter_by(user_id=user_id)
    if lesson_id is not None:
        query = query.filter_by(lesson_id=lesson_id)
    if challenge_id is not None:
        query = query.filter_by(challenge_id=challenge_id)
        
    recent_messages = query.order_by(ChatHistory.timestamp.desc()).limit(history_limit).all()
    recent_messages = recent_messages[::-1]
    return [{"role": msg.role, "content": msg.message} for msg in recent_messages]


def set_system_role(user_id, role):
    user = User.query.get(user_id)
    if user:
        user.system_role = role
        db.session.commit()

def get_system_role(user_id, lesson_id=None):
    if lesson_id:
        lesson = Lesson.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
        return lesson.system_role if lesson else None
    user = User.query.get(user_id)
    return user.system_role if user else None

def remove_latest_system_message(user_id, lesson_id=None):
    latest_system_message = ChatHistory.query.filter_by(user_id=user_id, lesson_id=lesson_id, role='system').order_by(ChatHistory.timestamp.desc()).first()
    if latest_system_message:
        db.session.delete(latest_system_message)
        db.session.commit()

def add_system_message(user_id, content, lesson_id=None):
    new_message = ChatHistory(
        user_id=user_id,
        role="system",
        message=content,
        system_role="system",
        challenge_id=None,
        lesson_id=lesson_id
    )
    db.session.add(new_message)
    db.session.commit()

def get_system_messages(user_id, lesson_id=None):
    system_chats = ChatHistory.query.filter_by(user_id=user_id, lesson_id=lesson_id, role='system').all()
    return [{"role": chat.role, "content": chat.message} for chat in system_chats]

def remove_latest_message_by_role(user_id, role):
    latest_message = ChatHistory.query.filter_by(user_id=user_id, role=role).order_by(ChatHistory.timestamp.desc()).first()
    if latest_message:
        db.session.delete(latest_message)
        db.session.commit()

def add_action(user_id, action_name, lesson_id=None):
    action = UserAction(user_id=user_id, action=action_name, lesson_id=lesson_id)
    db.session.add(action)
    db.session.commit()

def get_actions(user_id, lesson_id=None):
    actions = UserAction.query.filter_by(user_id=user_id, lesson_id=lesson_id).all()
    return [action.action for action in actions]

def add_achievement(achievement_name, description=None):
    achievement = Achievement(name=achievement_name, description=description)
    db.session.add(achievement)
    db.session.commit()

def grant_achievement_to_user(user_id, achievement_name):
    achievement = Achievement.query.filter_by(name=achievement_name).first()
    if achievement:
        user_achievement = UserAchievement(user_id=user_id, achievement_id=achievement.id)
        db.session.add(user_achievement)
        db.session.commit()

def get_user_achievements(user_id):
    achievements = db.session.query(Achievement.name).join(UserAchievement).filter(UserAchievement.user_id == user_id).all()
    return [achievement.name for achievement in achievements]

def set_profile(user_id, profile_data):
    user = User.query.get(user_id)
    if user:
        user.profile = profile_data
        db.session.commit()

def get_profile(user_id):
    user = User.query.get(user_id)
    return user.profile if user else None

def set_tutor(user_id, tutor_data):
    user = User.query.get(user_id)
    if user:
        user.ai_tutor_profile = tutor_data
        db.session.commit()

def get_tutor(user_id):
    user = User.query.get(user_id)
    return user.ai_tutor_profile if user else None

def add_challenge(user_id, challenge_name, completion_date=None):
    challenge = Challenge(user_id=user_id, challenge_name=challenge_name, completion_date=completion_date)
    db.session.add(challenge)
    db.session.commit()
    return challenge.id

def update_challenge(user_id, challenge_id, completion_date):
    challenge = Challenge.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if challenge:
        challenge.completion_date = completion_date

def add_lesson(user_id, lesson_name):
    lesson = Lesson(user_id=user_id, lesson_name=lesson_name, completion_date=None, system_role=None)
    db.session.add(lesson)
    db.session.commit()
    return lesson.id

def update_lesson(user_id, lesson_id, completion_date=None, system_role=None):
    lesson = Lesson.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
    if lesson:
        if completion_date:
            lesson.completion_date = completion_date
        elif system_role:
            lesson.system_role = system_role
    
    db.session.commit()

def get_user_challenges(user_id):
    return Challenge.query.filter_by(user_id=user_id).all()

def get_user_lessons(user_id):
    return Lesson.query.filter_by(user_id=user_id).all()

def get_user_lesson_name(user_id, lesson_id):
    return Lesson.query.filter_by(id=lesson_id, user_id=user_id).first().lesson_name

def get_completed_challenges(user_id):
    completed_challenges = Challenge.query.filter_by(user_id=user_id).filter(Challenge.completion_date.isnot(None)).all()
    return [challenge.challenge_name for challenge in completed_challenges]

def get_active_challenges(user_id):
    active_challenges = Challenge.query.filter_by(user_id=user_id).filter(Challenge.completion_date.is_(None)).all()
    return [challenge.challenge_name for challenge in active_challenges]

def get_completed_lessons(user_id):
    completed_lessons = Lesson.query.filter_by(user_id=user_id).filter(Lesson.completion_date.isnot(None)).all()
    return [lesson.lesson_name for lesson in completed_lessons]

def get_active_lessons(user_id):
    active_lessons = Lesson.query.filter_by(user_id=user_id).filter(Lesson.completion_date.is_(None)).all()
    return [lesson.lesson_name for lesson in active_lessons]

### CLEAR ###

def clear_user_chat_history(user_id):
    ChatHistory.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_challenges(user_id):
    Challenge.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_lessons(user_id):
    Lesson.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_actions(user_id):
    UserAction.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_achievements(user_id):
    UserAchievement.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_profile(user_id):
    user = User.query.get(user_id)
    if user:
        user.profile = None
        user.ai_tutor_profile = None
        user.current_lesson = None
        user.system_role = ''
        db.session.commit()

def reset_user_profile(user_id):
    clear_user_chat_history(user_id)
    clear_user_actions(user_id)
    clear_user_achievements(user_id)
    clear_user_challenges(user_id)
    clear_user_lessons(user_id)
    clear_user_profile(user_id)
