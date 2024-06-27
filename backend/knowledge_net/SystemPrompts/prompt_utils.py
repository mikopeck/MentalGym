import os
from database.library_handlers import get_library_room_names, get_library_content

def sys_library():
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    system_message_path = os.path.join(current_script_directory, f'GenerateLibraryRoomNames.txt')

    with open(system_message_path, 'r') as file:
        system_message = file.read()

    # if "{library-settings}" in system_message:
    #     system_message = system_message.replace("{user-profile}", "profile_content")

    return system_message

def sys_lib_room(library_id):
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    system_message_path = os.path.join(current_script_directory, f'GenerateLibraryRoom.txt')

    with open(system_message_path, 'r') as file:
        system_message = file.read()

    if "{library-map}" in system_message:
        lib_map, status = get_library_room_names(library_id)
        if status == 200:
            lib_map_str = ", ".join(lib_map)
            system_message = system_message.replace("{library-map}", lib_map_str)

    if "{library-context}" in system_message:
        content, status = get_library_content(library_id)
        if status == 200:
            content_str = "; ".join(f"{k}: {v}" for k, v in content.items())
            system_message = system_message.replace("{library-context}", content_str)

    return system_message