# routes/chat_routes.py

from flask import jsonify, request
from flask_login import login_required, current_user
from bleach import clean 

import database.db_handlers as dbh
from database.user_handler import increment_violations, is_within_limit
from system_guide import progress_challenge, progress_chat, progress_lesson
from openapi import moderate
import roles

def init_chat_routes(app):

    @app.route("/api/chat", methods=["GET", "POST"])
    @login_required
    def handle_chat():
        if request.method == "GET":
            lesson_id = request.args.get("lesson_id", None)
            challenge_id = request.args.get("challenge_id", None)
            return get_recent_chat(lesson_id, challenge_id)

        elif request.method == "POST":
            # rates
            within_limit, message = is_within_limit(current_user)
            if not within_limit:
                return jsonify({"error": message}), 429
            
            # sanitize & length
            userInput = request.form.get("message", "")
            userInput = clean(userInput)
            if len(userInput) > 1000:
                return jsonify({"error": "Message is too long. Maximum 1000 characters allowed."}), 400
            if len(userInput) < 1:
                return jsonify({"error": "No message."}), 400
            
            #moderate
            violation, message = moderate(userInput)
            if violation:
                increment_violations(current_user.id)
                return jsonify({"error": f"Message breaks our usage policy. Please check our guidelines.\n{message}"}), 400

            lesson_id = request.form.get("lesson_id", None)
            challenge_id = request.form.get("challenge_id", None)

            if lesson_id:
                return post_lesson_message(userInput, lesson_id)
            elif challenge_id:
                return post_challenge_message(userInput, challenge_id)
            else:
                return post_general_message(userInput)

    def get_recent_chat(lesson_id, challenge_id):
        actions = []
        if not challenge_id:
            actions = dbh.get_actions(current_user.id, lesson_id)
        else:
            actions = ["Leave challenge."]

        subheading, progress = get_subheading_and_progress(current_user, lesson_id, challenge_id)

        return jsonify(
            messages=dbh.get_recent_messages(current_user.id, lesson_id, challenge_id),
            actions=actions,
            subheading=subheading,
            progress=progress
        )


    def post_general_message(userInput):
        lesson_id = progress_chat(current_user.id, userInput)
        subheading, progress = get_subheading_and_progress(current_user, lesson_id, None)
        return jsonify(
            messages=dbh.get_recent_messages(current_user.id),
            actions=dbh.get_actions(current_user.id, lesson_id),
            redirect=lesson_id,
            subheading=subheading,
            progress=progress
        )

    def post_lesson_message(userInput, lesson_id):
        lesson_id = progress_lesson(current_user.id, userInput, lesson_id)
        subheading, progress = get_subheading_and_progress(current_user, lesson_id, None)
        return jsonify(
            messages=dbh.get_recent_messages(current_user.id, lesson_id),
            actions=dbh.get_actions(current_user.id, lesson_id),
            redirect=lesson_id,
            subheading=subheading,
            progress=progress
        )

    def post_challenge_message(userInput, challenge_id):
        progress_challenge(current_user.id, userInput, challenge_id)
        subheading, progress = get_subheading_and_progress(current_user, challenge_id=challenge_id)
        return jsonify(
            messages=dbh.get_recent_messages(current_user.id, challenge_id=challenge_id),
            actions=["Leave challenge."],
            subheading=subheading,
            progress=progress
        )
        


    def get_subheading_and_progress(user, lesson_id=None, challenge_id=None):
        subheading = None
        progress = None
        if lesson_id:
            subheading = dbh.get_user_lesson_name(user.id, lesson_id)
            if dbh.is_lesson_complete(user.id, lesson_id):
                progress = 1
            elif dbh.contains_quiz_message(user.id, lesson_id):
                progress = 0.7
            else:
                progress = ((len(dbh.get_recent_messages(user.id, lesson_id, challenge_id)) / 16) / 2) + 0.1
        if challenge_id:
            subheading = dbh.get_user_challenge_name(user.id, challenge_id)
            if dbh.is_challenge_complete(user.id, challenge_id):
                progress = 1
            else:
                progress = (len(dbh.get_recent_messages(user.id, lesson_id, challenge_id)) / 16) * 0.8
        else:
            role = dbh.get_system_role(user.id)
            if role == roles.ProfileGather:
                subheading = "Creating profile..."
                progress = (len(dbh.get_recent_messages(user.id, lesson_id, challenge_id)) / 16) * 0.9

        return subheading, progress
