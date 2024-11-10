from flask import jsonify
import numpy as np
from openapi import generate_response, get_embeddings, LESSON_TOKENS, GPT4
from message_handler import create_message
from knowledge_net.SystemPrompts.prompt_utils import sys_library, sys_lib_room, sys_first_room
import functions
from knowledge_net.math_utils import calculate_cosine_similarities
import database.library_handlers as lbh

def suggest_library_wing(user_id, selected_node, library_difficulty, language, language_difficulty,extra_context):
    def generate_rooms():
        system_msg = sys_library(library_difficulty, language, language_difficulty,extra_context)
        user_msg = f"Library Wing main topic: {selected_node}."
        function = [functions.GenerateLibraryRoomNames]
        function_call = {"name": function[0]['name']}
        messages = create_message(system_msg, user_msg)
        response = generate_response(user_id, messages, function, function_call, tokens=LESSON_TOKENS)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            return []
        rooms = functions.try_get_object(function[0], response_message)
        if rooms:
            room_list = rooms.get("room_names", [])
            return [room_obj.get("room_name", "").strip() for room_obj in room_list]
        return []

    attempts = 0
    max_attempts = 5
    room_names = generate_rooms()

    while len(room_names) < 24 and attempts < max_attempts:
        room_names = generate_rooms()
        attempts += 1

    if len(room_names) < 24:
        return None

    room_names= [selected_node]+room_names
    return room_names

# rooms
    
def fill_room(user_id, room_name, library_id):
    def generate_room_contents():
        system_msg = sys_lib_room(library_id)
        user_msg = room_name
        function = [functions.GenerateLibraryRoom]
        function_call = {"name": function[0]['name']}
        messages = create_message(system_msg, user_msg)
        response = generate_response(user_id, messages, function, function_call, tokens=LESSON_TOKENS, model=GPT4)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            return []
        room_contents = functions.try_get_object(function[0], response_message)
        if not room_contents:
            return []
        return room_contents
    
    attempts = 0
    max_attempts = 5
    room_contents = None
    result = jsonify(status="success")

    while not room_contents and attempts <= max_attempts and result.status != "success" :
        room_contents = generate_room_contents()
        attempts += 1

    return room_contents

def fill_room(user_id, subtopic, library_difficulty, language, language_difficulty, extra_context):
    def generate_room_contents():
        system_msg = sys_first_room(subtopic, library_difficulty, language, language_difficulty, extra_context)
        function = [functions.GenerateLibraryRoom]
        function_call = {"name": function[0]['name']}
        messages = create_message(system_msg, subtopic)
        response = generate_response(user_id, messages, function, function_call, tokens=LESSON_TOKENS, model=GPT4)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            return []
        room_contents = functions.try_get_object(function[0], response_message)
        if not room_contents:
            return []
        return room_contents
    
    attempts = 0
    max_attempts = 5
    room_contents = None
    result = jsonify(status="success")

    while not room_contents and attempts <= max_attempts and result.status != "success" :
        room_contents = generate_room_contents()
        attempts += 1

    return room_contents

def generate_room_content(user_id, subtopic, library_id):
    # Generate room content
    generated_content = fill_room(user_id, subtopic, library_id)
    if generated_content:
        return generated_content
    else:
        raise Exception("Failed to generate content")
    
def generate_room_content(user_id, topic, library_difficulty, language, language_difficulty, extra_context):
    # Generate room content
    generated_content = fill_room(user_id, topic, library_difficulty, language, language_difficulty, extra_context)
    if generated_content:
        return generated_content
    else:
        raise Exception("Failed to generate content")