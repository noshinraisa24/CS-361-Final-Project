from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Microservice URLs
TASK_SERVICE_URL = 'http://127.0.0.1:5002/tasks'
PROFILE_SERVICE_URL = 'http://127.0.0.1:5001/profile'
NOTIFICATION_SERVICE_URL = 'http://127.0.0.1:5003/notifications'
ANALYTICS_SERVICE_URL = 'http://127.0.0.1:5004/analytics'

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/home')
def home():
    # Fetch notifications from the Notification Microservice
    notifications = requests.get(NOTIFICATION_SERVICE_URL).json()
    return render_template('home.html', notifications=notifications)

@app.route('/buy_premium')
def buy_premium():
    return render_template('buy_premium.html')

# Add Task Route
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        task = {
            'title': request.form['title'],
            'description': request.form['description'],
            'due_date': request.form['due_date'],
            'completed': False
        }
        requests.post(TASK_SERVICE_URL, json=task)
        return redirect(url_for('your_tasks'))
    return render_template('add_task.html')

# View All Tasks
@app.route('/your_tasks')
def your_tasks():
    response = requests.get(TASK_SERVICE_URL)
    tasks = response.json() if response.status_code == 200 else []
    return render_template('your_tasks.html', tasks=tasks)

# Edit Task Route
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        updated_task = {
            'title': request.form['title'],
            'description': request.form['description'],
            'due_date': request.form['due_date']
        }
        requests.put(f"{TASK_SERVICE_URL}/{task_id}", json=updated_task)
        return redirect(url_for('your_tasks'))

    tasks = requests.get(TASK_SERVICE_URL).json()
    task = tasks[task_id] if 0 <= task_id < len(tasks) else None
    return render_template('edit_task.html', task=task, task_id=task_id)

# Delete Task Route
@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    requests.delete(f"{TASK_SERVICE_URL}/{task_id}")
    return redirect(url_for('your_tasks'))

# Route to mark a task as completed
@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    # Send completion request to Task Management Microservice
    requests.patch(f"{TASK_SERVICE_URL}/{task_id}/complete")
    return '', 204

# Profile management via microservice
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        profile = {
            'name': request.form['name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'country': request.form['country'],
            'job': request.form['job']
        }
        requests.post(PROFILE_SERVICE_URL, json=profile)
        return redirect(url_for('home'))

    response = requests.get(PROFILE_SERVICE_URL)
    profile = response.json() if response.text else {}
    return render_template('edit_profile.html', profile=profile)

@app.route('/help_support')
def help_support():
    support_info = {
        'phone': '555-123-4567',
        'email': 'support@taskmanager.com'
    }
    return render_template('help_support.html', support_info=support_info)

@app.route('/analytics')
def analytics():
    # Fetch analytics data from the Analytics Microservice
    analytics = requests.get(ANALYTICS_SERVICE_URL).json()
    return render_template('analytics.html', analytics=analytics)

if __name__ == '__main__':
    app.run(debug=True)






