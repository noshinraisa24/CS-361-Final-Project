from flask import Flask, jsonify
import json
import os
import datetime

app = Flask(__name__)
TASKS_FILE = '../task_service/tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

@app.route('/analytics', methods=['GET'])
def get_analytics():
    tasks = load_tasks()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for task in tasks if task.get('completed'))
    overdue_tasks = sum(1 for task in tasks if not task.get('completed') and datetime.datetime.strptime(task['due_date'], "%Y-%m-%d").date() < datetime.date.today())

    analytics = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,
    }

    return jsonify(analytics)

if __name__ == '__main__':
    app.run(port=5004)
