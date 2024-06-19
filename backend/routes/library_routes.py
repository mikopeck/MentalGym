# library_routes.py

import json
from flask import request, jsonify
from flask_login import current_user

import database.db_handlers as dbh
import knowledge_net.library_generator as lgn

def init_library_routes(app):

    @app.route("/api/library/generate", methods=["POST"])
    def generate_library():
        topic = request.json.get("topic")
        if not topic:
            return jsonify(status="error", message="No topic provided"), 400

        result = lgn.suggest_library_wing(current_user.id, topic)

        return jsonify(status="success", data=result)

    @app.route("/api/library/shelves", methods=["POST"])
    def generate_shelves():
        subtopic = request.json.get("subtopic")
        if not subtopic:
            return jsonify(status="error", message="No subtopic provided"), 400
        
        # Placeholder for your secret function 2 implementation
        result = dbh.secret_function_2(current_user.id, subtopic)
        
        return jsonify(status="success", data=result)
