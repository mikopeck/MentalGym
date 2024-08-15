from flask import jsonify
from flask_login import login_required, current_user
import database.db_handlers as dbh

def init_admin_routes(app):

    @app.route("/api/admin/feedback", methods=["GET"])
    @login_required
    def get_feedback():
        if current_user.email != 'mikopeck@gmail.com':
            return jsonify({"error": "Unauthorized access"}), 403

        feedback = dbh.get_all_feedback()
        return jsonify(feedback), 200

    @app.route("/api/admin/user-emails", methods=["GET"])
    @login_required
    def get_user_emails():
        # Check for specific admin user
        if current_user.email != 'mikopeck@gmail.com':
            return jsonify({"error": "Unauthorized access"}), 403

        emails = dbh.get_user_details()
        return jsonify(emails), 200