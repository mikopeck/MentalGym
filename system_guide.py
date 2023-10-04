# systemGuide.py
import db_handlers as db
import roles as roles
import functions as functions
import completion_tasks as cts
import message_handler as mh

def progress(user_id, user_message):
    lesson = process_user_message(user_id, user_message)
    db.clear_user_actions(user_id)

    # Progress chat
    current_sys_role = db.get_system_role(user_id)
    response = "No response."
    if current_sys_role == roles.ProfileGather:
        response = cts.gather_profile(user_id)
    elif current_sys_role == roles.SuggestContent:
        response = cts.suggest_content(user_id)
    elif current_sys_role == roles.LessonCreate:
        response = cts.lesson_create(user_id, lesson)
    elif current_sys_role == roles.LessonGuide:
        response = cts.lesson_guide(user_id)
    elif current_sys_role == roles.QuizCreate:
        response = cts.quiz_create(user_id)
    elif current_sys_role == roles.QuizFeedback:
        response = cts.quiz_feedback(user_id)

    # Progress roles and add actions
    current_sys_role = db.get_system_role(user_id)
    if current_sys_role == roles.LessonCreate:
        mh.update_system_role(user_id, roles.LessonGuide)
        current_sys_role = roles.LessonGuide

    if current_sys_role == roles.LessonGuide:
        db.add_action(user_id, "Continue to quiz.")
        db.add_action(user_id, "End lesson.")

    if current_sys_role == roles.QuizFeedback:
        db.add_action(user_id, "Continue to quiz.")
        db.add_action(user_id, "End lesson.")

    if current_sys_role == roles.QuizCreate:
        mh.update_system_role(user_id, roles.QuizFeedback)
        current_sys_role = roles.QuizFeedback
        db.add_action(user_id, "End lesson.")

    db.add_ai_response(user_id, response, current_sys_role)

def process_user_message(user_id, user_message):
    db.add_user_message(user_id, user_message)

    # Simple actions
    if user_message == "End lesson.":
        mh.update_system_role(user_id, roles.SuggestContent)
        return

    if user_message == "Continue to quiz.":
        mh.update_system_role(user_id, roles.QuizCreate)
        return

    # Complex actions
    if ':' not in user_message:
        return # No actions.
    
    action, content_name = user_message.split(':', 1)
    action = action.strip()
    current_actions = db.get_actions(user_id)

    if action.lower() == "start lesson":
        if user_message in current_actions:
            db.add_or_update_lesson(user_id, content_name)
            mh.update_system_role(user_id, roles.LessonCreate)
            return content_name
        else:
            print(f"Lesson '{content_name}' not found in available actions.")

    elif action.lower() == "accept challenge":
        if user_message in current_actions:
            db.add_or_update_challenge(user_id, content_name)
            print(f"Challenge '{content_name}' accepted.")
        else:
            print(f"Challenge '{content_name}' not found in available actions.")
