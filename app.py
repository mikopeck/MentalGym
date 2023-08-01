import os
import openai
from flask import Flask, redirect, render_template, request, url_for, session

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route("/", methods=("GET", "POST"))
def index():
    if 'messages' not in session:
        session['messages'] = [
            {
                "role": "system",
                "content": get_pychoanalysis_context()
            }
        ]

    if request.method == "POST":
        userInput = request.form["message"]
        session['messages'].append(
            {
                "role": "user",
                "content": userInput
            }
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=session['messages'],
            temperature=0.6
        )
        ai_message = response['choices'][0]['message']['content']
        session['messages'].append(
            {
                "role": "assistant",
                "content": ai_message
            }
        )
        print(session['messages'])
        session.modified = True
        return render_template("index.html", messages=session['messages'])

    return render_template("index.html", messages=session['messages'])

def get_pychoanalysis_context():
    with open('SystemPrompts/PsychoAnalysisRevised.txt', 'r') as file:
        return file.read()
    
@app.route("/reset", methods=["GET"])
def reset():
    session.pop('messages', None)
    return redirect(url_for("index"))