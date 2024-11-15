import os
from database.library_handlers import (
    get_library_room_names,
    get_library_content,
    get_library_settings,
    get_library_topic,
    get_library_guide
)

def create_difficulty_message(difficulty):
    messages = {
        "Easy": "The game is set to Easy difficulty, so reply with content which is straightforward and introductory.",
        "Normal": "The game is set to Medium difficulty, so reply with content which is moderately challenging.",
        "Hard": "The game is set to Hard difficulty. Design the content to be complex and demanding."
    }
    return messages.get(difficulty, "The game is set to Easy difficulty, so reply with content which is straightforward and introductory.")

def create_language_message(language, language_difficulty):
    messages = {
        "Easy": f"{language} is the chosen language, set to an easy level, so your reply should be simple and understandable for children and must be in {language}!",
        "Normal": f"{language} is the chosen language, set to a medium level, so your reply should be understandable to the average adult and must be in {language}!",
        "Hard": f"{language} is the chosen language, set to a hard level, so your reply should use rich vocabulary and may contain complex grammar and must be in {language}!"
    }
    return messages.get(language_difficulty, "English is the chosen language, set to a medium level, so your reply should be understandable to the average adult and must be in English!")

def sys_library(library_difficulty, language, language_difficulty, extra_context):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    system_message_path = os.path.join(
        current_script_directory, f"GenerateLibraryRoomNames.txt"
    )

    with open(system_message_path, "r") as file:
        system_message = file.read()

    difficulty_message = create_difficulty_message(library_difficulty)
    language_message = create_language_message(language, language_difficulty)
    meaningful_message = f"{difficulty_message} {language_message} Additional context: {extra_context}"

    if "{library-settings}" in system_message:
        system_message = system_message.replace("{library-settings}", meaningful_message)

    return system_message

def sys_lib_room(library_id):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    system_message_path = os.path.join(
        current_script_directory, f"GenerateLibraryRoom.txt"
    )

    with open(system_message_path, "r") as file:
        system_message = file.read()

    if "{base-persona}" in system_message:
        name = get_library_guide(library_id)
        base_persona_path = os.path.join(current_script_directory, f'Base{name}.txt')
        with open(base_persona_path, 'r') as file:
            persona = file.read()
            system_message = system_message.replace("{base-persona}", persona)

    if "{library-topic}" in system_message:
        lib_topic = get_library_topic(library_id)
        system_message = system_message.replace("{library-topic}", lib_topic)

    if "{library-map}" in system_message:
        lib_map, status = get_library_room_names(library_id)
        if status == 200:
            lib_map_str = ", ".join(lib_map)
            system_message = system_message.replace("{library-map}", lib_map_str)

    if "{library-settings}" in system_message:
        difficulty, language, language_difficulty, extra_context = get_library_settings(library_id)
        difficulty_message = create_difficulty_message(difficulty)
        language_message = create_language_message(language, language_difficulty)
        meaningful_message = f"{difficulty_message} {language_message} Additional context: {extra_context}"
        system_message = system_message.replace("{library-settings}", meaningful_message)

    if "{library-context}" in system_message:
        json_response, status = get_library_content(library_id)
        
        if status == 200:
            content_dict = json_response.get_json()
            content_str = content_dict['library_content']
            if content_str:
                system_message = system_message.replace("{library-context}", content_str)

    return system_message

def sys_first_room(subtopic, library_difficulty, language, language_difficulty, extra_context):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    system_message_path = os.path.join(
        current_script_directory, f"GenerateLibraryRoom.txt"
    )

    with open(system_message_path, "r") as file:
        system_message = file.read()

    if "{library-topic}" in system_message:
        system_message = system_message.replace("{library-topic}", subtopic)

    if "{library-map}" in system_message:
        system_message = system_message.replace("{library-map}", "Empty")

    if "{library-settings}" in system_message:
        difficulty_message = create_difficulty_message(library_difficulty)
        language_message = create_language_message(language, language_difficulty)
        meaningful_message = f"{difficulty_message} {language_message} Additional context: {extra_context}"
        system_message = system_message.replace("{library-settings}", meaningful_message)

    if "{library-context}" in system_message and extra_context:
        system_message = system_message.replace("{library-context}", "None")

    return system_message
