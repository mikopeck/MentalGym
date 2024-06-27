# library_routes.py

from flask import request, jsonify
from flask_login import current_user, AnonymousUserMixin

import database.library_handlers as lbh
import knowledge_net.library_generator as lgn

def init_library_routes(app):

    @app.route("/api/library/generate", methods=["POST"])
    def generate_library():
        topic = request.json.get("topic")
        if not topic:
            return jsonify(status="error", message="No topic provided"), 400

        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        result = lgn.suggest_library_wing(user_id, topic)
        
        room_names = [room for sublist in result for room in sublist]
        library_response, status_code = lbh.create_library(current_user.id, topic, room_names)

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
        
    @app.route("/api/library/shelves", methods=["POST"])
    def generate_shelves():
        data = request.get_json()
        subtopic = data.get("subtopic")
        library_id = data.get("libraryId")
        if not subtopic:
            return jsonify(status="error", message="No subtopic provided"), 400
        if not library_id:
            return jsonify(status="error", message="No library ID provided"), 400

        user_id = current_user.id if not isinstance(current_user, AnonymousUserMixin) else None
        result = lgn.fill_room(user_id, subtopic, library_id)
        return jsonify(status="success", data=result)
