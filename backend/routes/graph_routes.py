# routes/graph_routes.py

from flask import jsonify
from flask_login import login_required, current_user

from .. import db_handlers as dbh

def init_graph_routes(app):

    @app.route('/api/user-progress', methods=['GET'])
    @login_required
    def get_user_progress():
        #example
        data = {
            "labels": ["January", "February", "March", "April", "May"],
            "datasets": [
                {
                    "label": "Progress",
                    "backgroundColor": "#f87979",
                    "data": [40, 50, 55, 60, 70], 
                },
            ],
        }
        return jsonify({
            "status": "success",
            "progress": data
        })