# systemGuide.py

from flask import request

from openapi import generate_response, create_message
import db_handlers as db

ai_keywords = {
    "[PROFILE]",
    "[ACHIEVEMENT]",
    "[CHALLENGE]",
    "[LESSON]",
    "[END-COMPLETE]"
}

user_keywords = {
    "End lesson.",
    "Continue to quiz."
}

def initialize_session(user_id):
    message = "Hello! I'm Azalea, and I'm here to help you grow and achieve your goals. Is there anything you like to learn about today?"
    db.add_ai_message(user_id, message)

def process_ai_response(user_id, response):
    current_role = db.get_system_role(user_id)
    
    if current_role == "TutorInitialLesson":
        db.set_system_role(user_id, "TutorContinue")

    if current_role == "TutorContinue":
        db.add_action(user_id, "Continue to quiz.")
        db.add_action(user_id, "End lesson.")

    if current_role == "TutorQuiz":
        db.add_action(user_id, "End lesson.")

    last_assistant_message= response['choices'][0]['message']['content']

    keywords_present = [keyword for keyword in ai_keywords if keyword in last_assistant_message]
    if not keywords_present:
        return
    
    if "[PROFILE]" in keywords_present:
        user_profile = db.get_profile(user_id)
        if not user_profile:
            # First time profile
            new_profile = last_assistant_message.split("[PROFILE]", 1)[1]
            db.set_profile(user_id, new_profile)
            print("profile set:", new_profile)
            db.set_system_role(user_id, "TopicChoosing")
            change_system_message(user_id)
            db.remove_latest_message_by_role(user_id, "assistant")
            recent_messages = db.get_recent_messages(user_id)
            response = generate_response(recent_messages)
            db.add_ai_response(user_id, response)
            process_ai_response(user_id, response)
            return
        else:
            # Already has a profile
            current_role = db.get_system_role(user_id)
            db.set_system_role(user_id, "ProfileUpdate")
            profile_update_message = create_message(get_system_message(user_id), user_profile + last_assistant_message)
            response = generate_response(profile_update_message)
            ai_message = last_assistant_message.split("[PROFILE]", 1)[1]
            print("Profile updated: ", ai_message)
            db.set_system_role(user_id, current_role)
            change_system_message(user_id)

    if "[CHALLENGE]" in keywords_present:
        create_entries("challenge", user_id, last_assistant_message)

    if "[ACHIEVEMENT]" in keywords_present:
        create_entries("achievement", user_id, last_assistant_message)

    if "[LESSON]" in keywords_present:
        create_entries("lesson", user_id, last_assistant_message)
        
    if "[END-COMPLETE]" in keywords_present:
        db.add_completed_lesson(user_id, db.get_current_lesson(user_id))
        db.set_system_role(user_id, "TopicChoosing")
        change_system_message(user_id)

def create_entries(keyword, user_id, last_assistant_message):
    entries = extract_by_keyword(last_assistant_message, keyword)
    print(entries)
    user_prompt = ";".join(entries)

    current_role = db.get_system_role(user_id)
    if ";" in user_prompt:
        db.set_system_role(user_id, keyword + "Summaries")
    else:
        db.set_system_role(user_id, keyword + "Summary")

    message = create_message(get_system_message(user_id), user_prompt)
    response = generate_response(message)

    descriptions = response['choices'][0]['message']['content'].split(';')
    for description in descriptions:
        description = description.strip()
        if description:
            action_label = None
            if keyword == "challenge":
                action_label = "Accept challenge: " + description
            elif keyword == "lesson":
                action_label = "Start lesson: " + description
            elif keyword == "achievement":
                print("yay achieve")

            if action_label:
                db.add_action(user_id, action_label)

    db.set_system_role(user_id, current_role)


def extract_by_keyword(message, keyword):
    result = []
    keyword_with_brackets = f"[{keyword.upper()}]"
    
    # Check if the keyword_with_brackets is in the message
    if keyword_with_brackets not in message:
        return result

     # Iterate through the message by characters
    inside_section = False
    current_string = ''
    i = 0
    while i < len(message):
        # Check if the current position starts with the desired keyword
        if message[i:].startswith(keyword_with_brackets):
            inside_section = True
            i += len(keyword_with_brackets)
            continue

        # Check if the current position starts with any other keyword
        if inside_section and message[i:].startswith("["):
            inside_section = False
            result.append(current_string.strip())
            print("--------------appending", current_string)
            current_string = ''
            continue

        if inside_section:
            current_string += message[i]

        i += 1

    # Append any remaining text
    if current_string:
        result.append(current_string.strip())

    return result
    
def change_system_message(user_id):
    print("Updating system role: ", db.get_system_role(user_id))
    db.remove_latest_system_message(user_id)

    content = get_system_message(user_id)
    db.add_system_message(user_id, content)

def get_system_message(user_id):
    system_message = ""
    with open('SystemPrompts/' + db.get_system_role(user_id) + '.txt', 'r') as file:
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
        with open('SystemPrompts/profile.txt', 'r') as profile_file:
            profile_content = profile_file.read()
        system_message = system_message.replace("{profile}", profile_content)

    if "{profileFormat}" in system_message:
        with open('SystemPrompts/profileFormat.txt', 'r') as profile_format_file:
            profile_format_content = profile_format_file.read()
        system_message = system_message.replace("{profileFormat}", profile_format_content)

    return system_message

def prepare_session_messages(user_id):
    system_messages = db.get_system_messages(user_id)
    
    if not system_messages:
        change_system_message(user_id)
        system_messages = db.get_system_messages(user_id)

    limited_messages = db.get_recent_messages(user_id)
    has_system_message = any(msg['role'] == 'system' for msg in limited_messages)

    messages = system_messages + limited_messages if not has_system_message else limited_messages

    return messages

def process_user_message(user_id, user_message):
    if user_message == "End lesson.":
        db.set_system_role(user_id, "TopicChoosing")
        change_system_message(user_id)
        return

    if user_message == "Continue to quiz.":
        db.set_system_role(user_id, "TutorQuiz")
        change_system_message(user_id)
        return

    if ':' not in user_message:
        return
    
    action = user_message.split(':', 1)[0]
    action = action.strip()
    current_actions = db.get_actions(user_id)

    if action.lower() == "start lesson":
        if user_message in current_actions:
            db.set_current_lesson(user_id, user_message)
            print(f"Lesson '{user_message}' started.")
            
            # Prompt tutor creator with profile
            profile = db.get_profile(user_id)
            db.set_system_role(user_id, "TailorTutoring")
            tutor_create_message = create_message(get_system_message(user_id), profile)
            response = generate_response(tutor_create_message)
            db.set_tutor(user_id, response['choices'][0]['message']['content'])
            db.set_system_role(user_id, "TutorInitialLesson")
            change_system_message(user_id)
            return
        else:
            print(f"Lesson '{user_message}' not found.")

    elif action.lower() == "accept challenge":
        if user_message in current_actions:
            print(f"Challenge '{user_message}' accepted.")
        else:
            print(f"Challenge '{user_message}' not found.")