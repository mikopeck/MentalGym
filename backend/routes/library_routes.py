# library_routes.py

from flask import request, jsonify
from flask_login import current_user

import database.db_handlers as dbh
import database.library_handlers as lbh
import knowledge_net.library_generator as lgn

def init_library_routes(app):

    @app.route("/api/library/generate", methods=["POST"])
    def generate_library():
        topic = request.json.get("topic")
        if not topic:
            return jsonify(status="error", message="No topic provided"), 400

        result = lgn.suggest_library_wing(current_user.id, topic)
        
        room_names = [room for sublist in result for room in sublist]
        library_response, status_code = lbh.create_library(current_user.id, topic, room_names)

        if status_code == 201:
            library_id = library_response.get_json().get("library_id")
            return jsonify(status="success", library_id=library_id)
        else:
            return library_response

    @app.route("/api/library/shelves", methods=["POST"])
    def generate_shelves():
        subtopic = request.json.get("subtopic")
        if not subtopic:
            return jsonify(status="error", message="No subtopic provided"), 400
        
        # Placeholder for your secret function 2 implementation
        result = dbh.secret_function_2(current_user.id, subtopic)
        
        return jsonify(status="success", data=result)

    @app.route("/api/library/<int:library_id>", methods=["GET"])
    def get_library(library_id):
        library = lbh.get_library(library_id)
        if library:
            return jsonify(status="success", data=library.get_json())
        else:
            return jsonify(status="error", message="Library not found"), 404