# routes/profile_routes.py

from flask import request, jsonify
from flask_login import login_required, current_user

from .. import db_handlers as dbh

def init_profile_routes(app):

    @app.route("/api/profile", methods=["GET"])
    @login_required
    def get_profile_route():
        profile_data = {
            "user": dbh.get_profile(current_user.id),
            "tutor": dbh.get_tutor(current_user.id)
        }
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
