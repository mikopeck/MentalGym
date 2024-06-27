import numpy as np
from openapi import generate_response, get_embeddings
from message_handler import create_message
from knowledge_net.SystemPrompts.prompt_utils import sys_library, sys_lib_room
import roles, functions
from knowledge_net.math_utils import calculate_cosine_similarities

def suggest_library_wing(user_id, selected_node):
    def generate_rooms():
        system_msg = sys_library()
        user_msg = f"Library Wing main topic: {selected_node}."
        function = [functions.GenerateLibraryRoomNames]
        function_call = {"name": function[0]['name']}
        messages = create_message(system_msg, user_msg)
        response = generate_response(user_id, messages, function, function_call)
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

    room_names.append(selected_node)
    embeddings = get_embeddings(room_names)
    similarities = calculate_cosine_similarities(embeddings)
    library_data = map_rooms_to_grid(room_names, similarities)
    print_grid(library_data)
    return library_data

def map_rooms_to_grid(room_names, similarities):
    grid_size = 5
    center = (grid_size // 2, grid_size // 2)
    grid = np.full((grid_size, grid_size), None)

    # Place the main topic in the center
    main_topic_idx = len(room_names) - 1
    grid[center] = room_names[main_topic_idx]

    # Find the indices of the most similar rooms to the main topic
    main_similarities = similarities[main_topic_idx]
    sorted_indices = np.argsort(main_similarities)[::-1]

    # Ensure the main topic is not placed outside the center
    if sorted_indices[0] == main_topic_idx:
        sorted_indices = sorted_indices[1:]

    # Place the most similar rooms adjacent to the center
    adjacent_positions = [(2, 1), (2, 3), (1, 2), (3, 2)]
    for pos, idx in zip(adjacent_positions, sorted_indices[:4]):
        grid[pos] = room_names[idx]

    # Remove placed rooms from the remaining rooms list
    placed_rooms = {main_topic_idx}.union(set(sorted_indices[:4]))
    remaining_rooms = [idx for idx in sorted_indices[4:] if idx not in placed_rooms]

    def calculate_combined_similarity(idx, pos):
        combined_similarity = 0
        adjacent_positions = [
            (pos[0]-1, pos[1]), (pos[0]+1, pos[1]),
            (pos[0], pos[1]-1), (pos[0], pos[1]+1),
            (pos[0]-1, pos[1]-1), (pos[0]-1, pos[1]+1),
            (pos[0]+1, pos[1]-1), (pos[0]+1, pos[1]+1)
        ]
        for adj_pos in adjacent_positions:
            if 0 <= adj_pos[0] < grid_size and 0 <= adj_pos[1] < grid_size:
                adj_idx = grid[adj_pos]
                if adj_idx is not None:
                    adj_idx = room_names.index(adj_idx)
                    combined_similarity += similarities[idx, adj_idx]
        return combined_similarity

    # Place the most similar rooms diagonally to the center
    diagonal_positions = [(1, 1), (1, 3), (3, 1), (3, 3)]
    diagonal_room_indices = sorted(remaining_rooms[:4], key=lambda idx: max(calculate_combined_similarity(idx, pos) for pos in diagonal_positions), reverse=True)

    for pos, idx in zip(diagonal_positions, diagonal_room_indices):
        grid[pos] = room_names[idx]

    # Remove placed diagonal rooms from the remaining rooms list
    placed_rooms.update(diagonal_room_indices)
    remaining_rooms = [idx for idx in remaining_rooms if idx not in placed_rooms]

    remaining_positions = [
            (0, 2), (4, 2), (2, 0), (2, 4), # middles of the sides
            (0, 1), (4, 3),(0, 3), (4, 1),(1, 0), (3, 4),(1, 4), (3, 0),    # adjacent to the middles
            (4, 4),(0, 0),(0, 4),  (4, 0)  # corners
    ]
    for pos in remaining_positions:
            if grid[pos] is None:
                best_idx = max(remaining_rooms, key=lambda idx: calculate_combined_similarity(idx, pos))
                grid[pos] = room_names[best_idx]
                remaining_rooms.remove(best_idx)

    grid_list = grid.tolist()
    return grid_list

def print_grid(grid):
    for row in grid:
        row_str = ""
        for cell in row:
            if cell is None:
                row_str += "[    ]"
            else:
                row_str += f"[{cell[:24]}]"
        print(row_str)
    print("\n")


# rooms
    
def fill_room(user_id, room_name, library_id):
    def generate_room_contents():
        system_msg = sys_lib_room(library_id)
        user_msg = room_name
        function = [functions.GenerateLibraryRoom]
        function_call = {"name": function[0]['name']}
        messages = create_message(system_msg, user_msg)
        response = generate_response(user_id, messages, function, function_call)
        response_message = response["choices"][0]["message"]
        if not response_message.get("function_call"):
            return []
        room_contents = functions.try_get_object(function[0], response_message)
        if not room_contents:
            return []
        return room_contents
    
    attempts = 0
    max_attempts = 5
    room_contents = generate_room_contents()

    while not room_contents and attempts < max_attempts:
        room_contents = generate_room_contents()
        attempts += 1

    return room_contents
