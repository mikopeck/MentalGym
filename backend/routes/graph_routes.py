from flask import jsonify, request
from flask_login import login_required, current_user

from stats import get_line_graph_data, get_stats
from knowledge_net.graph_calc import get_graph_data
from knowledge_net.explore import suggest_lessons

def init_graph_routes(app):

    @app.route('/api/user-progress', methods=['GET'])
    @login_required
    def get_user_progress():
        line_graph_data = get_line_graph_data(current_user.id)
        stats = get_stats(current_user.id)

        data = {
            "lineGraph": line_graph_data,
            "totalCompleted": stats['totalCompleted'],
            "totalLessons": stats['totalLessons'],
            "activeLessons": stats['activeLessons'],
            "completedLessons": stats['completedLessons'],
            "totalLibrarys": stats['totalLibrarys'],
            "activeLibrarys": stats['activeLibrarys'],
            "completedLibrarys": stats['completedLibrarys'],
            "percentCompletedLessons": stats['percentCompletedLessons'],
            "percentCompletedLibrarys": stats['percentCompletedLibrarys'],
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
        try:
            data = get_graph_data(current_user.id)
            return jsonify({
                "status": "success",
                "data": data
            })
        except TypeError as e:
            print(f"Error: {e}")
            return jsonify({
                "status": "error",
                "message": "Keep learning and your knowledge will show here!"
            }), 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({
                "status": "error",
                "message": "An unexpected error occurred."
            }), 500

    
    @app.route('/api/explore', methods=['GET'])
    @login_required
    def explore():
        node_name = request.args.get('name', '')
        suggestions = suggest_lessons(current_user.id, node_name)
        return jsonify({"suggestions": suggestions})