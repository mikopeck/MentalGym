# routes/utility_routes.py

from flask import jsonify
from flask_login import login_required, current_user

import database.db_handlers as dbh
from message_handler import initialize_messages

def init_utility_routes(app):

    @app.route("/api/challenges", methods=["GET"])
    @login_required
    def get_challenges_route():
        challenges_data = {
            "active": dbh.get_active_challenges(current_user.id),
            "completed": dbh.get_completed_challenges(current_user.id)
        }
        return jsonify(status="success", challenges=challenges_data)

    @app.route("/api/lessons", methods=["GET"])
    @login_required
    def get_lessons_route():
        lessons_data = {
            "active": dbh.get_active_lessons(current_user.id),
            "completed": dbh.get_completed_lessons(current_user.id)
        }
        return jsonify(status="success", lessons=lessons_data)

    @app.route("/api/achievements", methods=["GET"])
    @login_required
    def get_achievements_route():
        achievements_data = dbh.get_user_achievements(current_user.id)
        return jsonify(status="success", achievements=achievements_data)

    @app.route("/reset", methods=["GET"])
    @login_required
    def reset():
        dbh.reset_user_profile(current_user.id)
        initialize_messages(current_user.id)
        return jsonify(messages=dbh.get_recent_messages(current_user.id), actions=[], status="success")