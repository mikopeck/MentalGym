from flask import jsonify, request
from flask_login import login_required, current_user

from stats import get_line_graph_data, get_pie_chart_data, get_stats
from knowledge_net.graph_calc import get_graph_data
from knowledge_net.explore import suggest_lessons

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
            "totalCompleted": stats['totalCompleted'],
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


    @app.route('/api/knowledge-net', methods=['GET'])
    @login_required
    def get_knowledge_graph():
        data = get_graph_data(current_user.id)
        print(data)
        return jsonify({
            "status": "success",
            "data": data
        })
    
    @app.route('/api/explore', methods=['GET'])
    @login_required
    def explore():
        node_name = request.args.get('name', '')
        suggestions = suggest_lessons(current_user.id, node_name)
        return jsonify({"suggestions": suggestions})