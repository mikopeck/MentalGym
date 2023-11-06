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
        rating = request.form.get("rating", None)  # If you have a rating system
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
