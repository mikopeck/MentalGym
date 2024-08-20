from openapi import generate_response
from message_handler import create_message, system_message
from utils import remove_emojis, remove_emojis_except_first
import roles, functions
import database.db_handlers as dbh

def suggest_lessons(user_id, selected_node):
    lesson_names = []
    system_msg = system_message(user_id, roles.ExploreTopic)
    user_msg = f"Suggest new topics connected to: {selected_node}."
    function = [functions.ExploreTopic]
    function_call = {"name": function[0]['name']}
    messages = create_message(system_msg, user_msg)
    response = generate_response(user_id, messages, function, function_call, temperature=0.7)
    response_message = response["choices"][0]["message"]
    if not response_message.get("function_call"):
        return []
    lessons = functions.try_get_object(function[0], response_message)
    if lessons:
        # Remove existing
        existing_actions = dbh.get_actions(user_id)
        for action in existing_actions:
            if action.startswith("Start lesson: "):
                dbh.remove_user_action(user_id, action)
        lesson_descriptions = lessons.get("lesson_suggestions", [])

        # Add new
        for lesson_obj in lesson_descriptions:
            lesson_text = remove_emojis(lesson_obj.get("lesson_name", "")).strip()
            lesson_emoji = lesson_obj.get("lesson_emoji", "")
            print(lesson_emoji)
            if lesson_emoji == "\",": # so many hax please help
                lesson_emoji = "🤔"
            lesson_name = remove_emojis_except_first(lesson_emoji+lesson_text)
            lesson_names.append(lesson_name)
            action_text = f"Start lesson: {lesson_name}"
            dbh.add_action(user_id, action_text)
            
    return lesson_names