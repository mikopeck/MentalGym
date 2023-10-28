from flask import jsonify
from flask_login import login_required, current_user

from stats import get_line_graph_data, get_pie_chart_data, get_stats

def init_graph_routes(app):

    @app.route('/api/user-progress', methods=['GET'])
    @login_required
    def get_user_progress():
        print("getting")
        line_graph_data = get_line_graph_data(current_user.id)
        pie_chart_data = get_pie_chart_data(current_user.id)
        stats = get_stats(current_user.id)

        data = {
            "lineGraph": line_graph_data,
            "pieChart": pie_chart_data,
            "totalContentCompleted": stats['totalContentCompleted'],
            "lessonsCompleted": stats['lessonsCompleted'],
            "challengesCompleted": stats['challengesCompleted'],
            "topTopics": stats['topTopics']
        }
        print(data)
        return jsonify({
            "status": "success",
            "progress": data
        })
