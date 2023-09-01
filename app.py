#app.py

import os
import openai
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, session, jsonify
from flask_session import Session

from systemGuide import process_ai_response, process_user_message, prepare_session_messages, change_system_message
from openapi import generate_response, append_assistant_response, initialize_session
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure the app for server-side sessions.
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'mental_gym:'
app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'session_data')

Session(app)

@app.route("/", methods=("GET", "POST"))
def index():
    if 'messages' not in session:
        session['system_role'] = "PsychoAnalysis"
        change_system_message(session)
        initialize_session(session)
        print("rendering", session)
        return render_template("index.html", messages=session['messages'])

    # Check if there's already a response pending.
    if session.get('response_pending', False):
        print("Response already pending")
        return render_template("index.html", messages=session['messages'], error="Response already pending")

    if request.method == "POST":
        # Set the flag to indicate that a response is pending.
        session['response_pending'] = True

        userInput = request.form["message"]
        process_user_message(userInput, session)
        
        session['messages'].append(
            {
                "role": "user",
                "content": userInput
            }
        )

        truncMsg = prepare_session_messages(session)
        response = generate_response(truncMsg)
        append_assistant_response(session, response)

        # Update role & other actions.
        process_ai_response(session)

        actions = session['actions']
        achievements = session['achievements']

        session_copy = session.copy() 
        session_copy.pop('messages', None)
        print(session_copy)

        session['response_pending'] = False
        session.modified = True
        return jsonify(messages=session['messages'], actions=actions, achievements=achievements)

    return render_template("index.html", messages=session['messages'])


@app.route("/reset", methods=["GET"])
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)