from flask import Flask, request, jsonify
from flask_cors import CORS
from services.task_service import TaskService
from data.database import init_db
import os

app = Flask(__name__)
CORS(app)

# Initialize database on startup
init_db()

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create new task with deadlines (TDRS-001-A)"""
    try:
        task_data = request.get_json()
        task = TaskService.create_task(task_data)
        return jsonify(task), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks with optional sorting (TDRS-001-A)"""
    try:
        sort_by = request.args.get('sortBy')
        order = request.args.get('order', 'asc')
        tasks = TaskService.get_tasks(sort_by, order)
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    """Get overdue tasks (TDRS-001-B)"""
    try:
        tasks = TaskService.get_overdue_tasks()
        return jsonify(tasks)
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
