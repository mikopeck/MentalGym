#app.py

import os
from dotenv import load_dotenv
import openai
from flask import Flask, redirect, render_template, request, url_for, session
from flask_session import Session

from systemGuide import update_system_role, get_system_message

load_dotenv()
app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.getenv('FLASK_SECRET_KEY')

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
        session['messages'] = [
            {
                "role": "system",
                "content": get_system_message(session['system_role'])
            }
        ]

    # Check if there's already a response pending.
    if session.get('response_pending', False):
        print("Response already pending")
        return render_template("index.html", messages=session['messages'], error="Response already pending")

    if request.method == "POST":
        print("Posting")
        # Set the flag to indicate that a response is pending.
        session['response_pending'] = True

        userInput = request.form["message"]
        session['messages'].append(
            {
                "role": "user",
                "content": userInput
            }
        )

        # Get the system message(s) from the session
        system_messages = [msg for msg in session['messages'] if msg['role'] == 'system']

        # Get the last 20 user and assistant messages
        user_assistant_messages = [msg for msg in session['messages'] if msg['role'] in ['user', 'assistant']][-20:]

        # Combine the system message(s) with the user and assistant messages
        truncMsg = {
            'messages': system_messages + user_assistant_messages
        }

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=truncMsg['messages'],
            top_p=0.1
        )
        ai_message = response['choices'][0]['message']['content']
        session['messages'].append(
            {
                "role": "assistant",
                "content": ai_message
            }
        )
        print(session['messages'])
        print(response['usage']['prompt_tokens'])
        session.modified = True

        # Update role
        update_system_role(session)

        # Clear the flag now that the response has been sent.
        session['response_pending'] = False

        return render_template("index.html", messages=session['messages'])

    return render_template("index.html", messages=session['messages'])


@app.route("/reset", methods=["GET"])
def reset():
    session.clear()
    return redirect(url_for("index"))
