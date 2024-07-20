import os
from database.library_handlers import (
    get_library_room_names,
    get_library_content,
    get_library_settings,
)

def create_difficulty_message(difficulty):
    messages = {
        "Easy": "The game is set to Easy difficulty. Please tailor the content to be straightforward and introductory.",
        "Medium": "The game is set to Medium difficulty. Please ensure the content is moderately challenging.",
        "Hard": "The game is set to Hard difficulty. Design the content to be complex and demanding."
    }
    return messages.get(difficulty, "Please check the difficulty setting as it is invalid.")

def create_language_message(language, language_difficulty):
    messages = {
        "Easy": f"{language} is the chosen language, set to an easy level. Ensure the language used is simple and clear.",
        "Medium": f"{language} is the chosen language, set to a medium level. Use moderately complex language constructions.",
        "Hard": f"{language} is the chosen language, set to a hard level. Employ advanced language structures and vocabulary."
    }
    return messages.get(language_difficulty, "Please check the language difficulty setting as it is invalid.")

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
        content, status = get_library_content(library_id)
        if status == 200:
            content_str = "; ".join(f"{k}: {v}" for k, v in content.items())
            system_message = system_message.replace("{library-context}", content_str)

    return system_message
