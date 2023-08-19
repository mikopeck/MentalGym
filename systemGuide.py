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

user_keywords ={
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
            update_system_message(session)
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
            ai_message = response['choices'][0]['message']['content']
            if "[PROFILE]" in ai_message:
                session['profile'] = last_assistant_message.split("[PROFILE]", 1)[1]
            else:
                print("Unsuccessful profile update", ai_message)
            session['system_role'] = role
            update_system_message(session)

    if "[CHALLENGE]" in keywords_present:
        create_entries("challenge", session, last_assistant_message)

    if "[ACHIEVEMENT]" in keywords_present:
        create_entries("achievement", session, last_assistant_message)

    if "[LESSON]" in keywords_present:
        create_entries("lesson", session, last_assistant_message)
        
    if "[END-COMPLETE]" in keywords_present:
        session.setdefault('achievements', [])
        session['achievement'].append(session['lesson'])
        session['system_role'] = "TopicChoosing"
        update_system_message(session)

    return

def create_entries(keyword, session, last_assistant_message):
    entries = extract_by_keyword(last_assistant_message, keyword)
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
        if inside_section and any(message[i:].startswith(other_keyword) for other_keyword in ai_keywords):
            inside_section = False
            result.append(current_string.strip())
            current_string = ''
            continue

        if inside_section:
            current_string += message[i]

        i += 1

    if current_string:
        result.append(current_string.strip())

    return result
    
def update_system_message(session):
    # Find the index of the last system message
    system_message_index = next((index for index, message in reversed(list(enumerate(session['messages']))) if message['role'] == 'system'), None)

    # Update the content of the last system message
    if system_message_index is not None:
        session['messages'][system_message_index]['content'] = get_system_message(session)
    else:
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

def process_user_message(user_message, session):
    if user_message == "End lesson.":
        session['system_role'] = "TopicChoosing"
        update_system_message(session)
        return

    if user_message == "Continue to quiz.":
        session['system_role'] = "TutorQuiz"
        update_system_message(session)
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
            update_system_message(session)
            return
        else:
            print(f"Lesson '{user_message}' not found.")

    elif action.lower() == "accept challenge":
        if user_message in session.get('challenges', []):
            session['current_challenge'] = user_message
            print(f"Challenge '{user_message}' accepted.")
        else:
            print(f"Challenge '{user_message}' not found.")