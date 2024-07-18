# library_routes.py

from flask import request, jsonify
from flask_login import current_user, AnonymousUserMixin

import database.library_handlers as lbh
import knowledge_net.library_generator as lgn
from database.user_handler import is_within_limit

def init_library_routes(app):

    @app.route("/api/library/generate", methods=["POST"])
    def generate_library():
        topic = request.json.get("topic")
        if not topic:
            return jsonify(status="error", message="No topic provided"), 400
        
        library_difficulty = request.json.get("libraryDifficulty")
        if not library_difficulty:
            library_difficulty = "Easy"

        language = request.json.get("language")
        if not language:
            language = "en"
        
        language_difficulty = request.json.get("languageDifficulty")
        if not language_difficulty:
            language_difficulty = "Normal"
            
        extra_context = request.json.get("extraContent")
        if not extra_context:
            existing_library = lbh.get_library_id(topic, library_difficulty, language, language_difficulty)
            if existing_library:
                return jsonify(status="success", library_id=existing_library)

        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        result = lgn.suggest_library_wing(user_id, topic)
        
        room_names = [room for sublist in result for room in sublist]
        library_response, status_code = lbh.create_library(user_id, topic, room_names, library_difficulty, language, language_difficulty)

        if status_code == 201:
            library_id = library_response.get_json().get("library_id")
            return jsonify(status="success", library_id=library_id)
        else:
            return library_response

    @app.route("/api/library/<int:library_id>", methods=["GET"])
    def get_library(library_id):
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        library = lbh.get_library(library_id, user_id)
        if library:
            return jsonify(status="success", data=library.get_json())
        else:
            return jsonify(status="error", message="Library not found"), 404
        
    @app.route("/api/library/room", methods=["POST"])
    def generate_room():
        data = request.get_json()
        subtopic = data.get("subtopic")
        library_id = data.get("libraryId")

        if not subtopic:
            return jsonify(status="error", message="No subtopic provided"), 400
        if not library_id:
            return jsonify(status="error", message="No library ID provided"), 400

        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None

        if user_id:
            within_limit, message = is_within_limit(current_user)
            if not within_limit:
                return jsonify({"error": message}), 429
        elif not lbh.is_center_room(library_id, subtopic):
            return jsonify(status="error", message="Please login to continue."), 400


        # Attempt to retrieve existing room contents
        existing_content = lbh.retrieve_library_room_contents(library_id, subtopic)
        if existing_content:
            return jsonify(status="success", data=existing_content)

        # If no content exists, generate new content
        generated_content = lgn.fill_room(user_id, subtopic, library_id)
        print(generated_content)
        if generated_content:
            return jsonify(status="success", data=generated_content)
        else:
            return jsonify(status="error", message="Failed to generate content"), 500
        
    @app.route("/api/library/shelves", methods=["POST"])
    def load_room():
        data = request.get_json()
        subtopic = data.get("subtopic")
        library_id = data.get("libraryId")

        if not subtopic:
            return jsonify(status="error", message="No subtopic provided"), 400
        if not library_id:
            return jsonify(status="error", message="No library ID provided"), 400

        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        # Attempt to retrieve existing room contents
        existing_content = lbh.retrieve_library_room_contents(library_id, subtopic)
        if existing_content:
            return jsonify(status="success", data=existing_content)

        # If no content exists, generate new content
        generated_content = lgn.fill_room(user_id, subtopic, library_id)
        print(generated_content)
        if generated_content:
            return jsonify(status="success", data=generated_content)
        else:
            return jsonify(status="error", message="Failed to generate content"), 500


    @app.route("/api/library/<int:library_id>/room/update", methods=["POST"])
    def update_room_state(library_id):
        if isinstance(current_user, AnonymousUserMixin):
            return jsonify({"status": "error", "message": "Please log in to update room states"}), 401

        user_id = current_user.id
        data = request.get_json()

        # Multiple rooms update (assuming the data format includes a list of rooms with their new states)
        if 'rooms' in data:
            responses = []
            for room in data['rooms']:
                room_name = room['room_name']
                new_state = room['new_state']
                answered_questions = room['answered_questions']
                current_question_index = room['current_question_index']
                response, status_code = lbh.update_library_room_state(user_id, library_id, room_name, new_state,answered_questions,current_question_index)
                if status_code != 200:
                    responses.append({"room_name": room_name, "status": "error", "message": response.get_json()['message']})
                else:
                    responses.append({"room_name": room_name, "status": "success"})
            return jsonify({"rooms": responses}), 200

        else:
            return jsonify({"status": "error", "message": "Invalid data provided"}), 400