# library_routes.py

from flask import request, jsonify
from flask_login import current_user, AnonymousUserMixin
from bleach import clean
from flask_executor import Executor

from openapi import moderate
import database.library_handlers as lbh
import knowledge_net.library_generator as lgn
from images.library_imager import generate_images_task
from database.user_handler import increment_violations, is_within_limit, check_generation_allowed, mark_generation_done

def init_library_routes(app):

    executor = Executor(app)

    @app.route("/api/library/generate", methods=["POST"])
    def generate_library():
        # User checks
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        if not user_id:
            ip = request.remote_addr
            if not check_generation_allowed(ip, 'library'):
                return jsonify(status="error", message="Library generation limit reached."), 403

        # Topic checks
        topic = request.json.get("topic")
        if not topic:
            return jsonify(status="error", message="No topic provided"), 400
        if len(topic) > 200:
                return jsonify({"error": "Topic is too long. Maximum 200 characters allowed."}), 400
        if len(topic) < 1:
                return jsonify({"error": "No message."}), 400
        
        # difficulty checks
        library_difficulty = request.json.get("libraryDifficulty")
        if not library_difficulty:
            library_difficulty = "Easy"
        else:
            library_difficulty = clean(library_difficulty)

        # language & langdifficulty checks
        language = request.json.get("language")
        if not language:
            language = "English"
        language_difficulty = request.json.get("languageDifficulty")
        if not language_difficulty:
            language_difficulty = "Normal"
            
        # Extra context checks
        extra_context = request.json.get("extraContent")
        if extra_context:
            extra_context = clean(extra_context)
        if extra_context and len(extra_context) > 200:
                return jsonify({"error": "Extra context is too long. Maximum 200 characters allowed."}), 400
        
        content_for_moderation = topic
        if extra_context:
            content_for_moderation += extra_context
        violation, message = moderate(content_for_moderation)
        if violation:
            if user_id:
                increment_violations(user_id)
            return jsonify({"error": f"Message breaks our usage policy. Please check our guidelines.\n{message}"}), 400
        
        if not extra_context:
            existing_library = lbh.get_library_id(topic, library_difficulty, language, language_difficulty)
            if existing_library:
                if not user_id:
                    mark_generation_done(ip, 'library')
                return jsonify(status="success", library_id=existing_library)

        result = lgn.suggest_library_wing(user_id, topic, library_difficulty, language, language_difficulty,extra_context)
        
        room_names = [room for sublist in result for room in sublist]
        library_response, status_code = lbh.create_library(user_id, topic, room_names, library_difficulty, language, language_difficulty)


        if status_code == 201:
            library_id = library_response.get_json().get("library_id")
            
            # start task of image generation
            executor.submit(generate_images_task, library_id)
            if not user_id:
                mark_generation_done(ip, 'library')
            return jsonify(status="success", library_id=library_id)
        else:
            return library_response

    @app.route("/api/library/<int:library_id>", methods=["GET"])
    def get_library(library_id):
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        library = lbh.get_library(library_id, user_id)
        
        response, status_code = lbh.has_default_image(library_id)
        if status_code != 200:
            return response 
    
        print(library.get_json().get("clicks")%4)
        print(library.get_json().get("clicks")%4 == 0)
        print(response.json['has_default_image'])
        if response.json['has_default_image'] and library.get_json().get("clicks")%4 == 0:
            executor.submit(generate_images_task, library_id)
            
        if library:
            return jsonify(status="success", data=library.get_json())
        else:
            return jsonify(status="error", message="Library not found"), 404
        
    @app.route("/api/library/room", methods=["POST"])
    def generate_room():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        data = request.get_json()
        subtopic = data.get("subtopic")
        library_id = data.get("libraryId")

        if not user_id:
            ip = request.remote_addr
            if not check_generation_allowed(ip, 'room'):
                return jsonify(status="error", message="Room generation limit reached."), 403

        if not subtopic:
            return jsonify(status="error", message="No subtopic provided"), 400
        if not library_id:
            return jsonify(status="error", message="No library ID provided"), 400


        if user_id:
            within_limit, message = is_within_limit(current_user)
            if not within_limit:
                return jsonify({"error": message}), 429
        elif not lbh.is_center_room(library_id, subtopic):
            return jsonify(status="error", message="Please login to continue."), 400


        # Attempt to retrieve existing room contents
        existing_content = lbh.retrieve_library_room_contents(library_id, subtopic)
        if existing_content:
            if not user_id:
                mark_generation_done(ip, 'room')
            return jsonify(status="success", data=existing_content)

        # If no content exists, generate new content
        generated_content = lgn.fill_room(user_id, subtopic, library_id)
        print(generated_content)
        if generated_content:
            if not user_id:
                mark_generation_done(ip, 'room')
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

        if 'score' in data:
            lbh.update_game_end(user_id, library_id, data['score'], False)

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
        
    @app.route("/api/library/end", methods=["POST"])
    def end_game():
        data = request.get_json()
        library_id = data.get('libraryId')
        score = data.get('score')
        
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        if not user_id:
            return jsonify({'status': 'error', 'message': "Not logged in..."}), 401
        
        if library_id is None or score is None:
            return jsonify({'status': 'error', 'message': 'Missing libraryId or score'}), 400

        try:
            response, status = lbh.update_game_end(user_id, library_id, score, True)
            return response, status
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
        
    @app.route("/api/libraries", methods=["GET"])
    def get_libraries():
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        return lbh.get_libraries_info(user_id)
    
    @app.route("/api/library/like", methods=["POST"])
    def like_library():
        data = request.get_json()
        return lbh.like_library(data.get('libraryId'))