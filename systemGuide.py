# systemGuide.py

def update_system_role(session):
    # Get the last assistant message from the session
    last_assistant_message = [message['content'] for message in session['messages'] if message['role'] == 'assistant'][-1]

    # Define the keywords and corresponding system roles
    keywords_to_role = {
        "[PROFILE]": "TopicChoosing",
        "[ACHIEVEMENT]": None, # Same role, just logging
        "[CHALLENGE]": None, # Same role, just logging
        "[LESSON]": "TutorGenerated",
        "[END-COMPLETE]": "TopicChoosing", # Same role, just logging
        "[END-MASTERED]": "TopicChoosing", # Same role, just logging
        "[END-USER]": "TopicChoosing", # Same role, just logging
        "[END-SYSTEM]": "TopicChoosing"  # Same role, just logging
    }

    # Check for the occurrence of keywords in the last assistant message
    for keyword, new_role in keywords_to_role.items():
        if keyword in last_assistant_message:
            # Logging for achievements and challenges
            if keyword == "[ACHIEVEMENT]":
                print("Achievement added to the user")
            elif keyword == "[CHALLENGE]":
                print("Challenge created for the user")
            
            # Update the system role if there's a new one associated with the keyword
            if new_role:
                session['system_role'] = new_role
                print(f"System role updated to {new_role}")
                break

    # Find the index of the last system message
    system_message_index = next((index for index, message in reversed(list(enumerate(session['messages']))) if message['role'] == 'system'), None)

    # Update the content of the last system message
    if system_message_index is not None:
        session['messages'][system_message_index]['content'] = get_system_message(session['system_role'])

    # If no keywords were found, the system role remains the same
    return


def get_system_message(filename):
    with open('SystemPrompts/'+filename+'.txt', 'r') as file:
        return file.read()
    