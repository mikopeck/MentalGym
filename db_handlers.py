from models import db, User, ChatHistory, CompletedChallenge, CompletedLesson, UserAction, UserActiveChallenge, Achievement, UserAchievement

def add_user_message(user_id, message_content):
    message = ChatHistory(user_id=user_id, message=message_content, role="user")
    db.session.add(message)
    db.session.commit()

def add_ai_response(user_id, response):
    ai_message = response['choices'][0]['message']['content']
    add_ai_message(user_id, ai_message)

def add_ai_message(user_id, message_content):
    message = ChatHistory(user_id=user_id, message=message_content, role="assistant")
    db.session.add(message)
    db.session.commit()

def get_recent_messages(user_id, limit=16):
    recent_messages = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
    recent_messages = recent_messages[::-1]
    return [{"role": msg.role, "content": msg.message} for msg in recent_messages]

def clear_chat_history(user_id):
    chat_records = ChatHistory.query.filter_by(user_id=user_id).all()
    for chat in chat_records:
        db.session.delete(chat)
    db.session.commit()

def set_system_role(user_id, role):
    user = User.query.get(user_id)
    if user:
        user.system_role = role
        db.session.commit()

def get_system_role(user_id):
    user = User.query.get(user_id)
    return user.system_role if user else None

def add_action(user_id, action_name):
    action = UserAction(user_id=user_id, action=action_name)
    db.session.add(action)
    db.session.commit()

def get_actions(user_id):
    actions = UserAction.query.filter_by(user_id=user_id).all()
    return [action.action for action in actions]

def clear_actions(user_id):
    actions = UserAction.query.filter_by(user_id=user_id).all()
    for action in actions:
        db.session.delete(action)
    db.session.commit()

def add_active_challenge(user_id, challenge_name):
    challenge = UserActiveChallenge(user_id=user_id, challenge=challenge_name)
    db.session.add(challenge)
    db.session.commit()

def remove_active_challenge(user_id, challenge_name):
    challenge = UserActiveChallenge.query.filter_by(user_id=user_id, challenge=challenge_name).first()
    if challenge:
        db.session.delete(challenge)
        db.session.commit()

def get_active_challenges(user_id):
    challenges = UserActiveChallenge.query.filter_by(user_id=user_id).all()
    return [challenge.challenge for challenge in challenges]

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

def remove_latest_system_message(user_id):
    latest_system_message = ChatHistory.query.filter_by(user_id=user_id, role='system').order_by(ChatHistory.timestamp.desc()).first()
    if latest_system_message:
        db.session.delete(latest_system_message)
        db.session.commit()

def add_system_message(user_id, content):
    new_message = ChatHistory(
        user_id=user_id,
        role="system",
        message=content
    )
    db.session.add(new_message)
    db.session.commit()

def get_system_messages(user_id):
    system_chats = ChatHistory.query.filter_by(user_id=user_id, role='system').all()
    return [{"role": chat.role, "content": chat.message} for chat in system_chats]

def remove_latest_message_by_role(user_id, role):
    latest_message = ChatHistory.query.filter_by(user_id=user_id, role=role).order_by(ChatHistory.timestamp.desc()).first()
    if latest_message:
        db.session.delete(latest_message)
        db.session.commit()

def add_completed_lesson(user_id, lesson_name):
    completed_lesson = CompletedLesson(user_id=user_id, lesson_name=lesson_name)
    db.session.add(completed_lesson)
    db.session.commit()

def set_current_lesson(user_id, lesson_name):
    user = User.query.get(user_id)
    if user:
        user.current_lesson = lesson_name
        db.session.commit()

def get_current_lesson(user_id):
    user = User.query.get(user_id)
    return user.current_lesson if user else None

def add_completed_challenge(user_id, challenge_name):
    completed_challenge = CompletedChallenge(user_id=user_id, challenge_name=challenge_name)
    db.session.add(completed_challenge)
    db.session.commit()

def get_completed_challenges(user_id):
    completed_challenges = CompletedChallenge.query.filter_by(user_id=user_id).all()
    return [challenge.challenge_name for challenge in completed_challenges]
