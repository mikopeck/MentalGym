#app.py

import os
import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from database.models import db, User

load_dotenv()
app = Flask(__name__, static_folder='../frontend/dist')
app.secret_key = os.getenv('FLASK_SECRET_KEY')
openai.api_key = os.getenv("OPENAI_API_KEY")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(user_id):
    session = db.session
    return session.get(User, int(user_id))

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'mysql+pymysql://root:password@localhost/mind_forge_ai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)
CORS(app)

# Routes
from routes.auth_routes import init_auth_routes
from routes.profile_routes import init_profile_routes
from routes.utility_routes import init_utility_routes
from routes.chat_routes import init_chat_routes
from routes.graph_routes import init_graph_routes

init_auth_routes(app)
init_profile_routes(app)
init_utility_routes(app)
init_chat_routes(app)
init_graph_routes(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify({"error": "User not authenticated"}), 401)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)