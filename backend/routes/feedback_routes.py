# routes/feedback_routes.py

from flask import jsonify, request
from flask_login import current_user, login_required
from bleach import clean 

import database.db_handlers as dbh

def init_feedback_routes(app):

    @app.route("/api/feedback", methods=["POST"])
    @login_required
    def handle_feedback():
        # sanitize & length
        userInput = request.form.get("message", "")
        rating = request.form.get("rating", None)
        userInput = clean(userInput)
        if len(userInput) > 2000:
            return jsonify({"error": "Message is too long. Maximum 2000 characters allowed."}), 400
        if (len(userInput) < 1) & (not rating):
            return jsonify({"error": "Please enter a message or rating."}), 400

        lesson_id = request.form.get("lesson_id", None)
        challenge_id = request.form.get("challenge_id", None)

        try:
            lesson_id = int(lesson_id) if lesson_id else None
            challenge_id = int(challenge_id) if challenge_id else None
            rating = int(rating) if rating else None
        except ValueError:
            return jsonify({"error": "Invalid lesson or challenge id."}), 400
        
        dbh.add_feedback(current_user.id, userInput, lesson_id, challenge_id, rating)
        return jsonify({"message": "Feedback submitted successfully."}), 201
    
    @app.route("/api/share", methods=["POST"])
    @login_required
    def share_lesson():
        data = request.json
        route_path = data.get('path')
        make_public = data.get('public', False)

        path_parts = route_path.split('/')
        if len(path_parts) >= 3 and path_parts[1] in ['challenge', 'lesson']:
            content_type = path_parts[1]
            try:
                content_id = int(path_parts[2])
            except ValueError:
                return jsonify({"error": "Invalid content ID"}), 400

            if content_type == 'challenge':
                if dbh.share_challenge(content_id, current_user.id):
                    if not dbh.publicise_challenge(content_id, current_user.id, make_public):
                        return jsonify({"error": "Failed to change challenge publicity"}), 400
                    return jsonify({"message": "Challenge shared successfully."})

                else:
                    return jsonify({"error": "Unauthorized"}), 401

            elif content_type == 'lesson':
                if dbh.share_lesson(content_id, current_user.id):
                    if not dbh.publicise_lesson(content_id, current_user.id, make_public):
                        return jsonify({"error": "Failed to change lesson publicity"}), 400
                    return jsonify({"message": "Lesson shared successfully."})

                else:
                    return jsonify({"error": "Unauthorized"}), 401
        else:
            return jsonify({"error": "Invalid route path"}), 400

