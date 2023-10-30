from flask import jsonify
from flask_login import login_required, current_user

from stats import get_line_graph_data, get_pie_chart_data, get_stats

def init_graph_routes(app):

    @app.route('/api/user-progress', methods=['GET'])
    @login_required
    def get_user_progress():
        line_graph_data = get_line_graph_data(current_user.id)
        pie_chart_data = get_pie_chart_data(current_user.id)
        stats = get_stats(current_user.id)

        data = {
            "lineGraph": line_graph_data,
            "pieChart": pie_chart_data,
            "totalContent": stats['totalContent'],
            "totalLessons": stats['totalLessons'],
            "activeLessons": stats['activeLessons'],
            "completedLessons": stats['completedLessons'],
            "totalChallenges": stats['totalChallenges'],
            "activeChallenges": stats['activeChallenges'],
            "completedChallenges": stats['completedChallenges'],
            "percentCompletedLessons": stats['percentCompletedLessons'],
            "percentCompletedChallenges": stats['percentCompletedChallenges'],
            "topTopics": stats['topTopics'],
            "maxStreak": stats['maxStreak'],
            "currentStreak": stats['currentStreak']
        }
        print(data)
        return jsonify({
            "status": "success",
            "progress": data
        })  

