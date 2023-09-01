# systemGuide.py

from flask import request
from openapi import generate_response, append_assistant_response, create_message

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

def process_ai_response(session):
    # Progress roles if needed.
    if session['system_role'] == "TutorInitialLesson":
        session['system_role'] = "TutorContinue"

    # Ensure default actions.
    session['actions'] = []
    if session['system_role'] == "TutorContinue":
        session['actions'].append("Continue to quiz.")
        session['actions'].append("End lesson.")

    if session['system_role'] == "TutorQuiz":
        session['actions'].append("End lesson.")

    # Get the last assistant message from the session
    last_assistant_message = [message['content'] for message in session['messages'] if message['role'] == 'assistant'][-1]

    # Check if any keywords are present in the last assistant message
    keywords_present = [keyword for keyword in ai_keywords if keyword in last_assistant_message]

    # If there were no keywords, return.
    if not keywords_present:
        return
    
    if "[PROFILE]" in keywords_present:        
        if 'profile' not in session:
            # First time profile
            session['profile'] = last_assistant_message.split("[PROFILE]", 1)[1]
            print("profile set:", session['profile'])
            session['messages'].pop()
            session['system_role'] = "TopicChoosing"
            change_system_message(session)
            response = generate_response(session['messages'])
            append_assistant_response(session, response)
            process_ai_response(session)
            return
        else:
            # Already has a profile
            role = session['system_role']
            session['system_role'] = "ProfileUpdate"
            profile_update_message = create_message(get_system_message(session), session['profile'] + last_assistant_message)
            response = generate_response(profile_update_message)
            ai_message = last_assistant_message.split("[PROFILE]", 1)[1]
            print("Profile updated: ", ai_message)
            session['system_role'] = role
            change_system_message(session)

    if "[CHALLENGE]" in keywords_present:
        create_entries("challenge", session, last_assistant_message)

    if "[ACHIEVEMENT]" in keywords_present:
        create_entries("achievement", session, last_assistant_message)

    if "[LESSON]" in keywords_present:
        create_entries("lesson", session, last_assistant_message)
        
    if "[END-COMPLETE]" in keywords_present:
        session.setdefault('achievements', [])
        session['achievement'].append(session['current_lesson'])
        session['system_role'] = "TopicChoosing"
        change_system_message(session)

    return

def create_entries(keyword, session, last_assistant_message):
    entries = extract_by_keyword(last_assistant_message, keyword)
    print(entries)
    user_prompt = ";".join(entries)

    role = session['system_role']
    if ";" in user_prompt:
        session['system_role'] = keyword + "Summaries"
    else:
        session['system_role'] = keyword + "Summary"

    message = create_message(get_system_message(session), user_prompt)
    response = generate_response(message)

    descriptions = response['choices'][0]['message']['content'].split(';')
    for description in descriptions:
        description = description.strip()
        if description:
            if keyword == "challenge":
                session['actions'].append("Accept challenge: "+description)
            if keyword == "lesson":
                session['actions'].append("Start lesson: "+description)
            if keyword == "achievement":
                session['achievements'].append(description)
    session['system_role'] = role

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
    
def change_system_message(session):
    print("Updating system role: ", session['system_role'])
    # remove old
    if 'messages' not in session:
        session.setdefault('messages', [])
    elif not session['messages']:
        system_message_index = next((index for index, message in reversed(list(enumerate(session['messages']))) if message['role'] == 'system'), None)
        if system_message_index is not None:
            del session['messages'][system_message_index]
    
    # add new
    session['messages'].append(
        {
            "role": "system",
            "content": get_system_message(session)
        }
    )

def get_system_message(session):
    # Default role.
    if 'system_role' not in session:
        session['system_role'] = "PsychoAnalysis"

    system_message = ""
    with open('SystemPrompts/' + session['system_role'] + '.txt', 'r') as file:
        system_message = file.read()

    # Replace all occurrences of {user-profile} with session['profile']
    profile_content = session['profile'] if 'profile' in session else '!!NO PROFILE!!'
    system_message = system_message.replace("{user-profile}", profile_content)

    # Replace all occurrences of {tutor-generated} with session['tutor']
    tutor_content = session['tutor'] if 'tutor' in session else '!!NO TUTOR!!'
    system_message = system_message.replace("{tutor-generated}", tutor_content)

    # Replace all occurrences of {profile} with the content of profile.txt
    with open('SystemPrompts/profile.txt', 'r') as profile_file:
        profile_content = profile_file.read()
    system_message = system_message.replace("{profile}", profile_content)

    # Replace all occurrences of {profileFormat} with the content of profileFormat.txt
    with open('SystemPrompts/profileFormat.txt', 'r') as profile_format_file:
        profile_format_content = profile_format_file.read()
    system_message = system_message.replace("{profileFormat}", profile_format_content)

    return system_message

def prepare_session_messages(session):
    system_messages = [msg for msg in session['messages'] if msg['role'] == 'system']
    if not system_messages:
        change_system_message(session)
        system_messages = [msg for msg in session['messages'] if msg['role'] == 'system']

    # Limit messages
    limited_messages = [msg for msg in session['messages']][-16:]

    if not [msg for msg in limited_messages if msg['role'] == 'system']:
        return system_messages + limited_messages
    else:
        return limited_messages

def process_user_message(user_message, session):
    if user_message == "End lesson.":
        session['system_role'] = "TopicChoosing"
        change_system_message(session)
        return

    if user_message == "Continue to quiz.":
        session['system_role'] = "TutorQuiz"
        change_system_message(session)
        return

    if ':' not in user_message:
        return
    
    action = user_message.split(':', 1)[0]
    action = action.strip()

    if action.lower() == "start lesson":
        if user_message in session.get('actions', []):
            session['current_lesson'] = user_message
            print(f"Lesson '{user_message}' started.")
            # Prompt tutor creator with profile
            session['system_role'] = "TailorTutoring"
            tutor_create_message = create_message(get_system_message(session), session['profile'])
            response = generate_response(tutor_create_message)
            session['tutor'] = response['choices'][0]['message']['content']
            session['system_role'] = "TutorInitialLesson"
            change_system_message(session)
            return
        else:
            print(f"Lesson '{user_message}' not found.")

    elif action.lower() == "accept challenge":
        if user_message in session.get('challenges', []):
            session['challenges'].append(user_message)
            print(f"Challenge '{user_message}' accepted.")
        else:
            print(f"Challenge '{user_message}' not found.")