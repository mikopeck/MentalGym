# library_routes.py

import random
from flask import request, jsonify
from flask_login import current_user, AnonymousUserMixin
from bleach import clean
from flask_executor import Executor

from openapi import moderate
import database.library_handlers as lbh
import knowledge_net.library_generator as lgn
from images.library_imager import generate_images_task, save_image
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
        topic = clean(topic)
        if len(topic) > 200:
            return jsonify({"error": "Topic is too long. Maximum 200 characters allowed."}), 400
        if len(topic) < 1:
            return jsonify({"error": "No message."}), 400

        # Difficulty checks
        library_difficulty = request.json.get("libraryDifficulty")
        VALID_DIFFICULTIES = ["Easy", "Normal", "Hard"]
        if not library_difficulty:
            library_difficulty = "Easy"
        else:
            library_difficulty = clean(library_difficulty)
            if library_difficulty not in VALID_DIFFICULTIES:
                library_difficulty = "Easy"

        # Guide checks
        guide = request.json.get("guide")
        VALID_GUIDES = ["Azalea", "Irona", "Bubbles", "Sterling"]
        if guide:
            guide = clean(guide)
        if not guide or guide not in VALID_GUIDES:
            guide = random.choice(VALID_GUIDES)

        # Language & language difficulty checks
        language = request.json.get("language")  # Add other supported languages
        if not language:
            language = "English"
        else:
            language = clean(language)

        language_difficulty = request.json.get("languageDifficulty")
        VALID_LANGUAGE_DIFFICULTIES = ["Easy", "Normal", "Hard"]
        if not language_difficulty:
            language_difficulty = "Normal"
        else:
            language_difficulty = clean(language_difficulty)
            if language_difficulty not in VALID_LANGUAGE_DIFFICULTIES:
                language_difficulty = "Normal"
        # Extra context checks
        extra_context = request.json.get("extraContent")
        if extra_context:
            extra_context = clean(extra_context)
            if len(extra_context) > 200:
                return jsonify({"error": "Extra context is too long. Maximum 200 characters allowed."}), 400

        # Check for existing library
        if not extra_context:
            existing_library = lbh.get_library_id(topic, library_difficulty, language, language_difficulty, guide)
            if existing_library:
                # Now check if first room exists
                existing_content = lbh.retrieve_library_room_contents(existing_library, topic)
                if existing_content:
                    return jsonify(status="success", library_id=existing_library)
                else:
                    try:
                        # Generate room content asynchronously
                        room_future = executor.submit(lgn.generate_libroom_content, user_id, topic, existing_library)
                        room_contents = room_future.result()
                        lbh.save_library_room_contents(existing_library, topic, room_contents)
                        return jsonify(status="success", library_id=existing_library)
                    except Exception as e:
                        return jsonify(status="error", message=f"Failed to generate room content {e}"), 500

        if not user_id:
            mark_generation_done(ip, 'library')
        
        # Start moderation task
        content_for_moderation = topic
        if extra_context:
            content_for_moderation += extra_context
        moderation_future = executor.submit(moderate, content_for_moderation)

        # Start library generation task
        room_names_future = executor.submit(lgn.suggest_library_wing, user_id, topic, library_difficulty, language, language_difficulty, extra_context)

        # Start image generation task
        img_url_future = executor.submit(generate_images_task, topic, library_difficulty, guide)

        # Generate first room content
        room_future = executor.submit(lgn.generate_room_content, user_id, topic, library_difficulty, language, language_difficulty, extra_context, guide)

        # Wait for moderation result
        violation, message = moderation_future.result()
        if violation:
            if user_id:
                increment_violations(user_id)
            return jsonify({"error": f"Message breaks our usage policy. Please check our guidelines.\n{message}"}), 400

        # Create the library
        room_names = room_names_future.result()
        library_response, status_code = lbh.create_library(user_id, topic, room_names, library_difficulty, language, language_difficulty, guide)
        if status_code == 201:
            library_id = library_response.get_json().get("library_id")
            img_url = img_url_future.result()
            print("saving image..")
            save_image(library_id, img_url)
        else:
            raise Exception("Library creation failed")

        try:
            room_contents = room_future.result()
            lbh.save_library_room_contents(library_id, topic, room_contents)
            library = lbh.get_library(library_id, user_id)

            return jsonify(status="success", library_data=library.get_json())
        except Exception as e:
            return jsonify(status="error", message="Failed to generate room content"), 500

    @app.route("/api/library/<int:library_id>", methods=["GET"])
    def get_library(library_id):
        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        library = lbh.get_library(library_id, user_id)

        if not library:
            return jsonify(status="error", message="Library not found"), 404

        # Check if the library has a default image and possibly trigger image generation
        response, status_code = lbh.has_default_image(library_id)
        if status_code != 200:
            return response

        # If there's a default image and the click count is divisible by 4, queue up image generation
        if response.json['has_default_image'] and library.get_json().get("clicks") % 4 == 0:
            executor.submit(generate_images_task, library_id)

        # Retrieve library data
        library_data = library.get_json()
        library_topic = library_data.get("library_topic")

        # Attempt to retrieve existing room contents
        room_data = lbh.retrieve_library_room_contents(library_id, library_topic)
        if not room_data:
            try:
                # If no content exists, generate the room content
                room_contents = lgn.generate_libroom_content(
                    user_id,
                    library_topic,
                    library_id
                )
                lbh.save_library_room_contents(library_id, library_topic, room_contents)
                room_data = room_contents
            except Exception as e:
                return jsonify(status="error", message="Failed to generate room content"), 500

        return jsonify(status="success", data=library_data, room_data=room_data)
        
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

        try:
            # If no content exists, generate new content
            generated_content = lgn.generate_libroom_content(user_id, subtopic, library_id)
            lbh.save_library_room_contents(library_id, subtopic, generated_content)
            existing_content = lbh.retrieve_library_room_contents(library_id, subtopic)
            if not user_id:
                mark_generation_done(ip, 'room')
            return jsonify(status="success", data=existing_content)
        except Exception as e:
            return jsonify(status="error", message=f"Failed to generate content {e}"), 500
    
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