import os
import json
import roles as roles
import functions as fns
import database.db_handlers as db

def initialize_messages(user_id):
    db.clear_user_chat_history(user_id)
    update_system_role(user_id, roles.ProfileGather)
    name = db.get_mentor_name(user_id)
    message = f"Hello! I'm {name}, and I'm here to help you grow and achieve your goals. What's your name?"
    if (name == "Azalea"):
        message = f"🐙 Hello there! I'm Azalea, your AI octopus guide to the wonders of learning. Imagine each of my tentacles as a path to new knowledge and skills! What's your name, and what exciting adventures can we embark on together in your learning journey?"
    elif (name == "Bubbles"):
        message = f"🌊 Hi there! I'm Bubbles, your AI otter guide in the river of knowledge. Let's splash into learning with joy and curiosity! 🦦 What's your name, and what are you excited to discover today?"
    elif (name == "Irona"):
        message = f"🦊 Welcome. I am Irona, your AI fox tutor. Here, discipline is key and humor sharp. Tell me your name and your ambition. Are you ready to push your limits and achieve excellence?"
    elif (name == "Sterling"):
        message = "Greetings, I am Sterling, your AI horse tutor. My approach is professional and direct. Please tell me your name and the subject you wish to excel in. Together, we'll pursue knowledge with precision and clarity."

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

def system_message(user_id, role_name = None ):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    if not role_name:
        role_name = db.get_system_role(user_id)

    system_prompts_path = os.path.join(current_script_directory, 'SystemPrompts')

    # Read the system message template
    system_message_path = os.path.join(system_prompts_path, f'{role_name}.txt')
    with open(system_message_path, 'r') as file:
        system_message = file.read()

    if "{user-profile}" in system_message:
        profile_content = json.dumps(db.get_user_info(user_id))
        if profile_content:
            system_message = system_message.replace("{user-profile}", profile_content)

    if "{tutor-generated}" in system_message:
        tutor_content = db.get_tutor(user_id)
        if tutor_content:
            system_message = system_message.replace("{tutor-generated}", tutor_content)

    if "{profile-function}" in system_message:
        system_message = system_message.replace("{profile-function}", str(fns.Profile))

    if "{base-persona}" in system_message:
        name = db.get_mentor_name(user_id)
        base_persona_path = os.path.join(system_prompts_path, f'Base{name}.txt')
        with open(base_persona_path, 'r') as file:
            persona = file.read()
            system_message = system_message.replace("{base-persona}", persona)

    if "{state}" in system_message:
        state = db.get_user_content(user_id)
        if state:
            system_message = system_message.replace("{state}", state)

    return system_message

def prepare_session_messages(user_id, lesson_id=None, challenge_id=None, limit=None):
    if not challenge_id:
        system_messages = db.get_system_messages(user_id, lesson_id)
    else: 
        system_messages = [{"role": "system", "content": system_message(user_id, roles.ChallengeGuide)+db.get_challenge_name(challenge_id)}]

    if not system_messages:
        initialize_messages(user_id)
        system_messages = db.get_system_messages(user_id)

    if limit:
        limited_messages = db.get_api_messages(user_id, lesson_id=lesson_id, challenge_id=challenge_id, limit=limit)
    else:
        limited_messages = db.get_api_messages(user_id, lesson_id=lesson_id, challenge_id=challenge_id)
    has_system_message = any(msg['role'] == 'system' for msg in limited_messages)

    messages = system_messages + limited_messages if not has_system_message else limited_messages
    return messages

def quiz_to_message(quiz):
    response = {}
    response["choices"] = [{}]
    response["choices"][0]["message"] = {"content": json.dumps(quiz)}
    return response
