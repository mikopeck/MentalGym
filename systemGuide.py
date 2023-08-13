# systemGuide.py

from flask import request
from openapi import generate_response, append_assistant_response

keywords = {
    "[PROFILE]",
    "[ACHIEVEMENT]",
    "[CHALLENGE]",
    "[LESSON]",
    "[END-COMPLETE]",
    "[END-USER]",
    "[END-SYSTEM]"
}

def process_ai_response(session):
    # Get the last assistant message from the session
    last_assistant_message = [message['content'] for message in session['messages'] if message['role'] == 'assistant'][-1]

    # Define the keywords and corresponding system roles

    # Check if any keywords are present in the last assistant message
    keywords_present = [keyword for keyword in keywords if keyword in last_assistant_message]

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
            profile_update_message = [
                {
                    "role": "system",
                    "content": get_system_message(session)
                },
                {
                    "role": "user",
                    "content": session['profile'] + last_assistant_message
                }
            ]
            response = generate_response(profile_update_message)
            ai_message = response['choices'][0]['message']['content']
            if "[PROFILE]" in ai_message:
                session['profile'] = last_assistant_message.split("[PROFILE]", 1)[1]
            else:
                print("Unsuccessful profile update", ai_message)
            session['system_role'] = role
            update_system_message(session)

    if "[CHALLENGE]" in keywords_present:
        create_entries("challenge", "ChallengeSummaries", session, last_assistant_message)

    if "[ACHIEVEMENT]" in keywords_present:
        create_entries("achievement", "AchievementSummaries", session, last_assistant_message)

    if "[LESSON]" in keywords_present:
        create_entries("lesson", "LessonSummaries", session, last_assistant_message)
    
    if "[END-USER]" in keywords_present or "[END-SYSTEM]" in keywords_present:
        session['system_role'] = "TopicChoosing"
        update_system_message(session)
        
    if "[END-COMPLETE]" in keywords_present:
        session.setdefault('achievements', [])
        session['achievement'].append(session['lesson'])
        session['system_role'] = "TopicChoosing"
        update_system_message(session)

    return

def create_entries(keyword, role_name, session, last_assistant_message):
    role = session['system_role']
    session['system_role'] = role_name

    #SPLIT MESSAGE BY KEYWORD
    entries = extract_by_keyword(last_assistant_message, keyword)
    user_prompt = ";".join(entries)

    create_message = [
        {
            "role": "system",
            "content": get_system_message(session)
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]
    response = generate_response(create_message)

    descriptions = response['choices'][0]['message']['content'].split(';')
    for description in descriptions:
        description = description.strip()
        if description:
            session[keyword + 's'].append(description)
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
        if inside_section and any(message[i:].startswith(other_keyword) for other_keyword in keywords):
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
    if ':' not in user_message:
        return
    action, description = user_message.split(':', 1)
    action = action.strip()
    description = description.strip()

    # Check if the action is to start a lesson
    if action.lower() == "start lesson":
        # Verify if the description is in the session's lessons
        if description in session.get('lessons', []):
            # Handle the logic to start the lesson with the given description
            session['current_lesson'] = description
            print(f"Lesson '{description}' started.")
        else:
            print(f"Lesson '{description}' not found.")

    # Check if the action is to accept a challenge
    elif action.lower() == "accept challenge":
        # Verify if the description is in the session's challenges
        if description in session.get('challenges', []):
            # Handle the logic to accept the challenge with the given description
            session['current_challenge'] = description
            print(f"Challenge '{description}' accepted.")
        else:
            print(f"Challenge '{description}' not found.")