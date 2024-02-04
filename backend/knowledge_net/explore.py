from openapi import generate_response
from message_handler import create_message, system_message
from utils import remove_emojis, remove_emojis_except_first
import roles, functions
import database.db_handlers as dbh

def suggest_lessons(user_id, selected_node):
    lesson_names = []
    system_msg = system_message(user_id, roles.ExploreTopic)
    user_msg = construct_user_message(user_id, selected_node)
    function = [functions.ExploreTopic]
    function_call = {"name": function[0]['name']}
    messages = create_message(system_msg, user_msg)
    response = generate_response(user_id, messages, function, function_call)
    response_message = response["choices"][0]["message"]
    if not response_message.get("function_call"):
        print("No content suggested...")
        return
    lessons = functions.try_get_object(function[0], response_message)
    if lessons:
        lesson_descriptions = lessons.get("lesson_suggestions", [])
        for lesson_obj in lesson_descriptions:
            lesson_text = remove_emojis(lesson_obj.get("lesson_name", "")).strip()
            lesson_emoji = lesson_obj.get("lesson_emoji", "")
            print(lesson_emoji)
            if lesson_emoji == "\",": # so many hax please help
                lesson_emoji = "🤔"
            lesson_name = remove_emojis_except_first(lesson_emoji+lesson_text)
            lesson_names.append(lesson_name)
            
    return lesson_names

def construct_user_message(user_id, selected_node):
    return get_user_activities(user_id) + f"\nThat is my topic history.\nSuggest lessons connected to: {selected_node}."

def get_user_activities(user_id):
    # Collect the results from each function
    completed_challenges = dbh.get_completed_challenges(user_id)
    active_challenges = dbh.get_active_challenges(user_id)
    completed_lessons = dbh.get_completed_lessons(user_id)
    active_lessons = dbh.get_active_lessons(user_id)

    # Combine all the results into a single list
    all_activities = completed_challenges + active_challenges + completed_lessons + active_lessons

    # Convert the list of dictionaries to a string with comma-separated values
    return ', '.join(str(activity) for activity in all_activities)
