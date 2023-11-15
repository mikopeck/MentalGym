import os
import json
import roles as roles
import functions as fns
import database.db_handlers as db

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

def update_system_role(user_id, role: roles, lesson_id=None):
    if lesson_id:
        db.update_lesson(user_id, lesson_id,system_role=role)
    else:
        db.set_system_role(user_id, role)
    print(f"Updating system role{lesson_id}: {role}")
    db.remove_latest_system_message(user_id, lesson_id)
    db.add_system_message(user_id, system_message(user_id, role), lesson_id)

def system_message(user_id, file_name = None ):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    if not file_name:
        file_name = db.get_system_role(user_id)

    system_prompts_path = os.path.join(current_script_directory, 'SystemPrompts')

    # Read the system message template
    system_message_path = os.path.join(system_prompts_path, f'{file_name}.txt')
    with open(system_message_path, 'r') as file:
        system_message = file.read()

    if "{user-profile}" in system_message:
        profile_content = json.dumps(db.get_user_context(user_id))
        if profile_content:
            system_message = system_message.replace("{user-profile}", profile_content)

    if "{tutor-generated}" in system_message:
        tutor_content = db.get_tutor(user_id)
        if tutor_content:
            system_message = system_message.replace("{tutor-generated}", tutor_content)

    if "{profile-function}" in system_message:
        system_message = system_message.replace("{profile-function}", str(fns.Profile))

    if "{base-persona}" in system_message:
        base_persona_path = os.path.join(system_prompts_path, 'BaseAzalea.txt')
        with open(base_persona_path, 'r') as file:
            persona = file.read()
            system_message = system_message.replace("{base-persona}", persona)

    if "{state}" in system_message:
        state = db.get_user_content(user_id)
        if state:
            system_message = system_message.replace("{state}", state)

    return system_message

def prepare_session_messages(user_id, lesson_id=None, challenge_id=None):
    if not challenge_id:
        system_messages = db.get_system_messages(user_id, lesson_id)
    else: 
        system_messages = [{"role": "system", "content": system_message(user_id, roles.ChallengeGuide)+db.get_user_challenge_name(user_id, challenge_id)}]

    if not system_messages:
        initialize_messages(user_id)
        system_messages = db.get_system_messages(user_id)

    limited_messages = db.get_api_messages(user_id, lesson_id=lesson_id, challenge_id=challenge_id)
    has_system_message = any(msg['role'] == 'system' for msg in limited_messages)

    messages = system_messages + limited_messages if not has_system_message else limited_messages
    return messages