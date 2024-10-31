from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
TASKS_FILE = 'tasks.json'


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)

# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json
    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    return jsonify({'status': 'Task added successfully'}), 201

# Route to edit an existing task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def edit_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id].update(request.json)  # Update task details
        save_tasks(tasks)
        return jsonify({'status': 'Task updated successfully'})
    else:
        return jsonify({'error': 'Task not found'}), 404

# Route to delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
        return jsonify({'status': 'Task deleted successfully'})
    else:
        return jsonify({'error': 'Task not found'}), 404


@app.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    tasks = load_tasks()
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = True
        save_tasks(tasks)
        return jsonify({'status': 'Task marked as completed'})
    else:
        return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(port=5002)

