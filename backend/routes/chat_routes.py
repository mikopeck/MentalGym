# routes/chat_routes.py

from flask import jsonify, request
from flask_login import login_required, current_user

import db_handlers as dbh
from system_guide import progress_challenge, progress_chat, progress_lesson

def init_chat_routes(app):

    @app.route("/api/chat", methods=["GET", "POST"])
    @login_required
    def handle_chat():
        if request.method == "GET":
            lesson_id = request.args.get("lesson_id", None)
            challenge_id = request.args.get("challenge_id", None)
            return get_recent_chat(lesson_id, challenge_id)

        elif request.method == "POST":
            lesson_id = request.form.get("lesson_id", None)
            challenge_id = request.form.get("challenge_id", None)
            userInput = request.form.get("message", "")

            if lesson_id:
                return post_lesson_message(userInput, lesson_id)
            elif challenge_id:
                return post_challenge_message(userInput, challenge_id)
            else:
                return post_general_message(userInput)

    def get_recent_chat(lesson_id, challenge_id):
        actions = []
        if not challenge_id:
            actions=dbh.get_actions(current_user.id, lesson_id)

        subheading = None
        if lesson_id:
            subheading = dbh.get_user_lesson_name(current_user.id, lesson_id)
        if challenge_id:
            subheading = dbh.get_user_challenge_name(current_user.id, challenge_id)

        return jsonify(
            messages=dbh.get_recent_messages(current_user.id, lesson_id, challenge_id),
            actions=actions,
            subheading=subheading
        )

    def post_general_message(userInput):
        lesson_id = progress_chat(current_user.id, userInput)
        return jsonify(
            messages=dbh.get_recent_messages(current_user.id),
            actions=dbh.get_actions(current_user.id, lesson_id),
            redirect=lesson_id
        )

    def post_lesson_message(userInput, lesson_id):
        lesson_id = progress_lesson(current_user.id, userInput, lesson_id)
        return jsonify(
            messages=dbh.get_recent_messages(current_user.id, lesson_id=lesson_id),
            actions=dbh.get_actions(current_user.id, lesson_id),
            redirect=lesson_id
        )

    def post_challenge_message(userInput, challenge_id):
        progress_challenge(current_user.id, userInput, challenge_id)
        return jsonify(
            messages=dbh.get_recent_messages(current_user.id, challenge_id=challenge_id),
            actions=dbh.get_actions(current_user.id)
        )