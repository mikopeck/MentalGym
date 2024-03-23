from database.models import db, User, ChatHistory, Challenge, Lesson, UserAction, Achievement, UserAchievement, Feedback
from utils import decode_if_needed, extract_single_emoji
from datetime import datetime

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

def add_ai_response(user_id, response, sys_role, challenge_id=None, lesson_id=None, message_type="message"):
    ai_message = response['choices'][0]['message']['content']
    add_ai_message(user_id, ai_message, sys_role, challenge_id, lesson_id, message_type)

def add_ai_message(user_id, message_content, sys_role, challenge_id=None, lesson_id=None, message_type="message"):
    message = ChatHistory(
        user_id=user_id, 
        message=decode_if_needed(message_content), 
        role="assistant", 
        system_role=sys_role,
        challenge_id=challenge_id,
        lesson_id=lesson_id,
        message_type=message_type
    )
    db.session.add(message)
    db.session.commit()

def add_content_message(user_id, content_name, challenge_id=None, lesson_id=None):
    system_role = None
    if challenge_id:
        system_role = f"challenge/{challenge_id}"
    elif lesson_id:
        system_role = f"lesson/{lesson_id}"
    else:
        print("Content ID not passed error.")

    message = ChatHistory(
        user_id=user_id, 
        message=content_name, 
        role=system_role, 
        system_role=system_role,
        challenge_id=None,
        lesson_id=None
    )
    db.session.add(message)
    db.session.commit()

def edit_content_message_to_completed(user_id, challenge_id=None, lesson_id=None):
    if challenge_id:
        message = ChatHistory.query.filter_by(user_id=user_id, system_role=f"challenge/{challenge_id}").first()
    elif lesson_id:
        message = ChatHistory.query.filter_by(user_id=user_id, system_role=f"lesson/{lesson_id}").first()
    if not message:
        return

    message.role += "?completed"
    message.system_role += "?completed"
    db.session.commit()

def add_completion_message(user_id, challenge_id=None, lesson_id=None):
    edit_content_message_to_completed(user_id, challenge_id, lesson_id)
    completion_message = ChatHistory(
        user_id=user_id,
        message="Completed!",
        role="complete",
        system_role="complete",
        challenge_id=challenge_id,
        lesson_id=lesson_id
    )
    
    db.session.add(completion_message)
    db.session.commit()

def get_recent_messages(user_id, lesson_id=None, challenge_id=None, limit=history_limit):
    query = ChatHistory.query.filter_by(user_id=user_id, lesson_id=lesson_id, challenge_id=challenge_id)
    recent_messages = query.order_by(ChatHistory.id.desc()).limit(limit).all()
    recent_messages = recent_messages[::-1]
    return [{"role": msg.role, "content": msg.message, "type": msg.message_type} for msg in recent_messages]

def get_content_messages(lesson_id, challenge_id, limit=history_limit):
    query = ChatHistory.query.filter_by(lesson_id=lesson_id, challenge_id=challenge_id)
    recent_messages = query.order_by(ChatHistory.id.desc()).limit(limit).all()
    recent_messages = recent_messages[::-1]
    return [{"role": msg.role, "content": msg.message, "type": msg.message_type} for msg in recent_messages]

def get_api_messages(user_id, lesson_id=None, challenge_id=None, limit=history_limit):
    query = ChatHistory.query.filter_by(user_id=user_id, lesson_id=lesson_id, challenge_id=challenge_id)
    
    valid_roles = ['system', 'assistant', 'user', 'function']
    query = query.filter(ChatHistory.role.in_(valid_roles))

    recent_messages = query.order_by(ChatHistory.id.desc()).limit(limit).all()
    recent_messages = recent_messages[::-1]
    return [{"role": msg.role, "content": msg.message} for msg in recent_messages]

def set_system_role(user_id, role):
    user = User.query.get(user_id)
    if user:
        user.system_role = role
        db.session.commit()

def get_system_role(user_id, lesson_id=None):
    if lesson_id:
        lesson = Lesson.query.filter_by(user_id=user_id, id=lesson_id).first()
        return lesson.system_role if lesson else None
    user = User.query.get(user_id)
    return user.system_role if user else None

def set_mentor_name(user_id, name):
    user = User.query.get(user_id)
    if user:
        user.mentor_name = name
        db.session.commit()

def get_mentor_name(user_id):
    user = User.query.get(user_id)
    return user.mentor_name if user and user.mentor_name else "Azalea"

def remove_latest_system_message(user_id, lesson_id=None):
    latest_system_message = ChatHistory.query.filter_by(user_id=user_id, lesson_id=lesson_id, role='system').order_by(ChatHistory.id.desc()).first()
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
    latest_message = ChatHistory.query.filter_by(user_id=user_id, role=role).order_by(ChatHistory.id.desc()).first()
    if latest_message:
        db.session.delete(latest_message)
        db.session.commit()
        
def get_latest_message_by_role(user_id, role):
    latest_message = ChatHistory.query.filter_by(user_id=user_id, role=role).order_by(ChatHistory.id.desc()).first()
    return latest_message.message if latest_message else None

def remove_score_from_answer(user_id, message):
    latest_message = ChatHistory.query.filter_by(user_id=user_id, role="user").order_by(ChatHistory.id.desc()).first()
    latest_message.message = message
    db.session.commit()

def contains_quiz_message(lesson_id):
    return bool(ChatHistory.query.filter_by(lesson_id=lesson_id, message_type="quiz").order_by(ChatHistory.id.desc()).first())

def complete_quiz_message(user_id, lesson_id, score):
    latest_quiz = ChatHistory.query.filter_by(user_id=user_id, lesson_id=lesson_id, message_type="quiz").order_by(ChatHistory.id.desc()).first()
    latest_quiz.message = score + latest_quiz.message
    db.session.commit()

def add_action(user_id, action_name, lesson_id=None):
    existing_action = UserAction.query.filter_by(user_id=user_id, action=action_name, lesson_id=lesson_id).first()
    if not existing_action:
        action = UserAction(user_id=user_id, action=action_name, lesson_id=lesson_id)
        db.session.add(action)
        db.session.commit()


def get_actions(user_id, lesson_id=None):
    actions = UserAction.query.filter_by(user_id=user_id, lesson_id=lesson_id).all()
    return [action.action for action in actions]

def remove_user_action(user_id, action_name, lesson_id=None):
    action = UserAction.query.filter_by(user_id=user_id, action=action_name, lesson_id=lesson_id)
    action.delete()

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

# Profile
def get_complete_user_data(user_id):
    user = User.query.get(user_id)
    if not user:
        return None

    user_data = {
        "email": user.email,
        "tier": user.tier,
        "user": user.profile,
        "tutor": user.ai_tutor_profile,
    }
    return user_data

def set_profile(user_id, profile_data):
    user = User.query.get(user_id)
    if user:
        user.profile = profile_data
        db.session.commit()

def get_profile(user_id):
    user = User.query.get(user_id)
    return user.profile if user else None

def get_user_info(user_id):
    user = User.query.get(user_id)
    return user.as_dict() if user else None

def set_tutor(user_id, tutor_data):
    user = User.query.get(user_id)
    if user:
        user.ai_tutor_profile = tutor_data
        db.session.commit()

def get_tutor(user_id):
    user = User.query.get(user_id)
    return user.ai_tutor_profile if user else None

def get_user_content(user_id):
    user = User.query.get(user_id)
    return user.current_content if user else None

def set_user_content(user_id, content_description):
    user = User.query.get(user_id)
    if user:
        user.current_content = content_description
        db.session.commit()

def add_challenge(user_id, challenge_name, user_started = True):
    if not extract_single_emoji(challenge_name):
        challenge_name = f"⛰️{challenge_name}"
    challenge = Challenge(user_id=user_id, challenge_name=challenge_name, completion_date=None)
    db.session.add(challenge)
    db.session.commit()
    add_content_message(user_id, challenge_name,challenge_id=challenge.id)
    add_ai_message(user_id, f"Share your progress 📈, ask for a plan 📆, or some just guidance 🧭.\n\n I'm here to help you complete the challenge:\n{challenge_name}", "challenge", challenge.id)
    if user_started:
        set_user_content(user_id, f"started challenge {challenge_name}")
    else:
        set_user_content(user_id, f"was given (by you) challenge {challenge_name}")
    return challenge.id

def update_challenge(user_id, challenge_id):
    challenge = Challenge.query.filter_by(user_id=user_id, id=challenge_id).first()
    if challenge:
        set_user_content(user_id, f"completed challenge {challenge.challenge_name}")
        challenge.completion_date = datetime.now()

def is_challenge_complete(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    return challenge.completion_date is not None if challenge else False


def add_lesson(user_id, lesson_name, user_started = True):
    existing_lesson = Lesson.query.filter_by(user_id=user_id, lesson_name=lesson_name).first()
    if existing_lesson:
        return False, existing_lesson.id
    
    if not extract_single_emoji(lesson_name):
        lesson_name = f"🤔{lesson_name}"
    lesson = Lesson(user_id=user_id, lesson_name=lesson_name, completion_date=None, system_role=None)
    db.session.add(lesson)
    db.session.commit()
    add_content_message(user_id, lesson_name,lesson_id=lesson.id)
    if user_started:
        set_user_content(user_id, f"started lesson {lesson_name}")
    else:
        set_user_content(user_id, f"was given (by you) lesson {lesson_name}")
    return True, lesson.id

def update_lesson(user_id, lesson_id, completion_date=None, system_role=None):
    lesson = Lesson.query.filter_by(user_id=user_id, id=lesson_id).first()
    if lesson:
        if completion_date:
            set_user_content(user_id, f"completed lesson {lesson.lesson_name}")
            lesson.completion_date = completion_date
        elif system_role:
            if system_role == "LessonCreate":
                set_user_content(user_id, f"started lesson {lesson.lesson_name}")
            else:
                set_user_content(user_id, f"worked on but not completed lesson {lesson.lesson_name}")
            lesson.system_role = system_role
    
    db.session.commit()

def is_lesson_complete(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    return lesson.completion_date is not None if lesson else False

def is_lesson_shared(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first()
    return bool(lesson and lesson.shared)

def is_challenge_shared(challenge_id):
    challenge = Challenge.query.filter_by(id=challenge_id).first()
    return bool(challenge and challenge.shared)

def publicise_challenge(challenge_id, user_id, make_public):
    challenge = Challenge.query.get(challenge_id)
    if challenge and challenge.user_id == user_id:
        challenge.public = make_public
        db.session.commit()
        return True
    return False

def publicise_lesson(lesson_id, user_id, make_public):
    lesson = Lesson.query.get(lesson_id)
    if lesson and lesson.user_id == user_id:
        lesson.public = make_public
        db.session.commit()
        return True
    return False

def get_public_lessons():
    public_lessons = Lesson.query.filter_by(public=True, shared=True).limit(16).all()
    return [lesson.as_dict() for lesson in public_lessons]

def get_public_challenges():
    public_challenges = Challenge.query.filter_by(public=True, shared=True).limit(16).all()
    return [challenge.as_dict() for challenge in public_challenges]

def get_user_challenges(user_id):
    return Challenge.query.filter_by(user_id=user_id).all()

def get_challenge_name(challenge_id):
    return Challenge.query.filter_by(id=challenge_id).first().challenge_name
    
def get_user_lessons(user_id):
    return Lesson.query.filter_by(user_id=user_id).all()

def get_lesson_name(lesson_id):
    return Lesson.query.filter_by(id=lesson_id).first().lesson_name

def get_completed_challenges(user_id):
    completed_challenges = Challenge.query.filter_by(user_id=user_id).filter(Challenge.completion_date.isnot(None)).all()
    return [challenge.as_dict() for challenge in completed_challenges]

def get_active_challenges(user_id):
    active_challenges = Challenge.query.filter_by(user_id=user_id).filter(Challenge.completion_date.is_(None)).all()
    return [challenge.as_dict() for challenge in active_challenges]

def get_completed_lessons(user_id):
    completed_lessons = Lesson.query.filter_by(user_id=user_id).filter(Lesson.completion_date.isnot(None)).all()
    return [lesson.as_dict() for lesson in completed_lessons]

def get_active_lessons(user_id):
    active_lessons = Lesson.query.filter_by(user_id=user_id).filter(Lesson.completion_date.is_(None)).all()
    return [lesson.as_dict() for lesson in active_lessons]

def get_user_lesson_names(user_id):
    lessons = Lesson.query.filter_by(user_id=user_id).all()
    return [lesson.lesson_name for lesson in lessons]

def share_challenge(challenge_id, user_id):
        challenge = Challenge.query.get(challenge_id)
        if challenge and challenge.user_id == user_id:
            challenge.shared = True
            db.session.commit()
            return True
        return False

def share_lesson(lesson_id, user_id):
    lesson = Lesson.query.get(lesson_id)
    if lesson and lesson.user_id == user_id:
        lesson.shared = True
        db.session.commit()
        return True
    return False

def add_feedback(user_id, content, lesson_id=None, challenge_id=None, rating=None):
    new_feedback = Feedback(
        user_id=user_id,
        content=content,
        lesson_id=lesson_id,
        challenge_id=challenge_id,
        rating=rating
    )
    db.session.add(new_feedback)
    db.session.commit()

def get_all_feedback():
    feedback_list = Feedback.query.all()
    return [feedback.as_dict() for feedback in feedback_list]

def get_all_user_emails():
    users = User.query.with_entities(User.email).all()
    email_list = [user.email for user in users]
    return email_list


### GRAPHS ###

def get_offered_lessons(user_id):
    actions = UserAction.query.filter_by(user_id=user_id).filter(UserAction.action.like('Start lesson:%')).all()
    offered_lessons = [action.action.split('Start lesson:')[1].strip() for action in actions]
    return offered_lessons

def get_offered_challenges(user_id):
    actions = UserAction.query.filter_by(user_id=user_id).filter(UserAction.action.like('Accept challenge:%')).all()
    offered_challenges = [action.action.split('Accept challenge:')[1].strip() for action in actions]
    return offered_challenges

def user_knowledge_net_info(user_id):
    user = User.query.get(user_id)
    if not user:
        return None

    user_data = {
        "profile": user.profile,
        "active_challenges": [{
            'id': challenge.id,
            'name': challenge.challenge_name
        } for challenge in sorted(
            [c for c in user.challenges if not c.completion_date], 
            key=lambda x: x.id, reverse=True)[:10]
        ],
        "completed_challenges": [{
            'id': challenge.id,
            'name': challenge.challenge_name
        } for challenge in sorted(
            [c for c in user.challenges if c.completion_date], 
            key=lambda x: x.id, reverse=True)[:20]
        ],
        "active_lessons": [{
            'id': lesson.id,
            'name': lesson.lesson_name
        } for lesson in sorted(
            [l for l in user.lessons if not l.completion_date], 
            key=lambda x: x.id, reverse=True)[:30]
        ],
        "completed_lessons": [{
            'id': lesson.id,
            'name': lesson.lesson_name
        } for lesson in sorted(
            [l for l in user.lessons if l.completion_date], 
            key=lambda x: x.id, reverse=True)[:100]
        ],
        "latest_action": user.current_content
    }

    # Add offered lessons and challenges
    user_data['offered_lessons'] = get_offered_lessons(user_id)
    user_data['offered_challenges'] = get_offered_challenges(user_id)

    return user_data

### CLEAR ###

def clear_user_chat_history(user_id):
    ChatHistory.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_challenges(user_id):
    Challenge.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_lessons(user_id):
    # MUST CLEAR all actions first.
    Lesson.query.filter_by(user_id=user_id).delete()
    db.session.commit()

def clear_user_actions(user_id, lesson_id=None):
    UserAction.query.filter_by(user_id=user_id, lesson_id=lesson_id).delete()
    db.session.commit()

def clear_all_user_actions(user_id):
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
    clear_all_user_actions(user_id)
    clear_user_achievements(user_id)
    clear_user_challenges(user_id)
    clear_user_lessons(user_id)
    clear_user_profile(user_id)
