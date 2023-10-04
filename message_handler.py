import roles as roles
import functions as fns
import db_handlers as db

def initialize_messages(user_id):
    update_system_role(user_id, roles.ProfileGather)
    message = "Hello! I'm Azalea, and I'm here to help you grow and achieve your goals. Is there anything you like to learn about today?"
    db.add_ai_message(user_id, message, roles.ProfileGather)

def create_message(system_message, user_message):
    return [
        {
            "role": "system",
            "content": system_message
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

def user_message(message):
    return [
        {
            "role": "user",
            "content": message
        }
    ]

def update_system_role(user_id, role: roles):
    db.set_system_role(user_id, role)
    print("Updating system role: ", role)
    db.remove_latest_system_message(user_id)
    db.add_system_message(user_id, system_message(user_id))

def system_message(user_id, file_name:roles = None ):
    if not file_name:
        file_name = db.get_system_role(user_id)

    system_message = ""
    with open('SystemPrompts/' + file_name + '.txt', 'r') as file:
        system_message = file.read()

    if "{user-profile}" in system_message:
        profile_content = db.get_profile(user_id)
        if profile_content:
            system_message = system_message.replace("{user-profile}", profile_content)

    if "{tutor-generated}" in system_message:
        tutor_content = db.get_tutor(user_id)
        if tutor_content:
            system_message = system_message.replace("{tutor-generated}", tutor_content)

    if "{profile}" in system_message:
        system_message = system_message.replace("{profile}", str(fns.Profile))

    return system_message

def prepare_session_messages(user_id):
    system_messages = db.get_system_messages(user_id)
    if not system_messages:
        initialize_messages(user_id)
        system_messages = db.get_system_messages(user_id)

    limited_messages = db.get_api_messages(user_id)
    has_system_message = any(msg['role'] == 'system' for msg in limited_messages)

    messages = system_messages + limited_messages if not has_system_message else limited_messages

    return messages