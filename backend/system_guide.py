# systemGuide.py
import database.db_handlers as db
import roles as roles
import functions as functions
import completion_tasks as cts
import message_handler as mh

def progress_chat(user_id, user_message):
    db.add_user_message(user_id, user_message)
    return progress(user_id, detect_content_actions(user_id, user_message))

def progress_lesson(user_id, user_message, lesson_id):
    db.add_user_message(user_id, user_message, lesson_id=lesson_id)
    if user_message == "Leave lesson.":
        return None
    elif user_message == "Continue to quiz.":
        mh.update_system_role(user_id, roles.QuizCreate, lesson_id)
    return progress(user_id, lesson_id)

def progress_challenge(user_id, user_message, challenge_id):
    db.add_user_message(user_id, user_message, challenge_id=challenge_id)
    response = cts.challenge_progress(user_id, challenge_id)
    db.add_ai_response(user_id, response, roles.ChallengeGuide, challenge_id=challenge_id)

def progress(user_id, lesson_id):
    db.clear_user_actions(user_id, lesson_id)

    # Progress chat
    current_sys_role = db.get_system_role(user_id, lesson_id)
    response = "No response."
    if current_sys_role == roles.ProfileGather:
        response, lesson_id = cts.gather_profile(user_id)
    elif current_sys_role == roles.SuggestContent:
        response, lesson_id = cts.suggest_content(user_id)
    elif current_sys_role == roles.AfterContent:
        response, lesson_id = cts.after_content(user_id)
    elif current_sys_role == roles.LessonCreate:
        response, lesson_id = cts.lesson_create(user_id, lesson_id)
    elif current_sys_role == roles.QuizCreate:
        response, lesson_id = cts.quiz_create(user_id, lesson_id)
    elif current_sys_role == roles.QuizFeedback:
        response, lesson_id = cts.quiz_feedback(user_id, lesson_id)
        if not response:
            return lesson_id # Completed lesson.
    else:
        if lesson_id:
            response, lesson_id = cts.lesson_guide(user_id, lesson_id)
        else:
            print(" Unknown role!!", current_sys_role)
            response, lesson_id = cts.suggest_content(user_id)

    # Progress roles and add actions
    current_sys_role = db.get_system_role(user_id, lesson_id)
    if (current_sys_role == roles.LessonCreate) | (current_sys_role == roles.QuizFeedback):
        mh.update_system_role(user_id, roles.LessonGuide, lesson_id)
        current_sys_role = roles.LessonGuide

    if current_sys_role == roles.LessonGuide:
        db.add_action(user_id, "Continue to quiz.", lesson_id)
        db.add_action(user_id, "Leave lesson.", lesson_id)

    if current_sys_role == roles.QuizCreate:
        mh.update_system_role(user_id, roles.QuizFeedback, lesson_id)
        current_sys_role = roles.QuizFeedback
        db.add_action(user_id, "Leave lesson.", lesson_id)

    if current_sys_role == roles.AfterContent:
        mh.update_system_role(user_id, roles.SuggestContent)
        current_sys_role = roles.SuggestContent
        db.add_action(user_id, "Suggest.")

    if (current_sys_role == roles.LessonGuide) | (current_sys_role == roles.QuizFeedback):
        db.add_ai_response(user_id, response, current_sys_role, lesson_id=lesson_id)
        return lesson_id
    else: 
        db.add_ai_response(user_id, response, current_sys_role)

def detect_content_actions(user_id, user_message):
    if (user_message == "Continue...") & ("Continue..." in db.get_actions(user_id)):
        mh.update_system_role(user_id, roles.AfterContent)
        return None

    if ':' not in user_message:
        return None
    
    action, content_name = user_message.split(':', 1)
    action = action.strip()
    current_actions = db.get_actions(user_id)

    if action.lower() == "start lesson":
        if user_message in current_actions:
            lesson_id = db.add_lesson(user_id, content_name)
            db.remove_user_action(user_id,user_message)
            db.add_action(user_id, "Continue...")
            mh.update_system_role(user_id, roles.LessonCreate, lesson_id)
            return lesson_id
        else:
            print(f"Lesson '{content_name}' not found in available actions.")

    elif action.lower() == "accept challenge":
        if user_message in current_actions:
            db.add_challenge(user_id, content_name)
            db.remove_user_action(user_id,user_message)
            mh.update_system_role(user_id, roles.AfterContent)
        else:
            print(f"Challenge '{content_name}' not found in available actions.")
