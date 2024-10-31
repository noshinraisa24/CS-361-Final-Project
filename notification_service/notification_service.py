from flask import Flask, jsonify
import json
import datetime
import os

app = Flask(__name__)
TASKS_FILE = '../task_service/tasks.json'

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

@app.route('/notifications', methods=['GET'])
def get_notifications():
    tasks = load_tasks()
    notifications = []
    today = datetime.date.today()

    for task in tasks:
        due_date = datetime.datetime.strptime(task['due_date'], "%Y-%m-%d").date()
        if 0 <= (due_date - today).days <= 1 and not task['completed']:
            notifications.append(f"Task '{task['title']}' is due soon!")

    return jsonify(notifications)

if __name__ == '__main__':
    app.run(port=5003)
