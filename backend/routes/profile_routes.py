# routes/profile_routes.py

from flask import request, jsonify
from flask_login import login_required, current_user

import database.db_handlers as dbh
from database.user_handler import get_user_tier, set_user_tier

def init_profile_routes(app):

    @app.route("/api/profile", methods=["GET"])
    @login_required
    def get_profile_route():
        profile_data = dbh.get_complete_user_data(current_user.id)
        print(profile_data)
        return jsonify(status="success", profile=profile_data)

    @app.route("/api/profile/user", methods=["POST"])
    @login_required
    def update_user_profile():
        new_data = request.json.get("data")
        dbh.set_profile(current_user.id, new_data)
        return jsonify(status="success")

    @app.route("/api/profile/tutor", methods=["POST"])
    @login_required
    def update_tutor_profile():
        new_data = request.json.get("data")
        dbh.set_tutor(current_user.id, new_data)
        return jsonify(status="success")

    @app.route("/api/plan", methods=["GET"])
    @login_required
    def get_user_plan():
        tier = get_user_tier(current_user.id)
        return jsonify(status="success", tier=tier)

    @app.route("/api/plan", methods=["POST"])
    @login_required
    def set_user_plan():
        data = request.json
        tierName = data.get('tier')
        if not tierName:
            return jsonify(status="error", message=""), 400

        set_user_tier(current_user.id, tierName)
        return jsonify(status="success")