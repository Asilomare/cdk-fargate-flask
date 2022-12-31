import os
import json
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

event_data = os.environ['SQLALCHEMY_DATABASE_URI']
event_json = json.loads(event_data)

username = event_json['username']
password = event_json['password']
host = event_json['host']
port = event_json['port']
database = event_json['dbInstanceIdentifier']

# Construct the connection string
connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string

db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String, nullable=False)

# Create the routes for the application

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = Task(description=request.form['description'],
                status=request.form['status'],
                due_date=request.form['due_date'],
                priority=request.form['priority'])
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.status = 'Complete'
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>')
def edit_task(task_id):
    task = Task.query.get(task_id)
    return render_template('edit.html', task=task)

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get(task_id)
    task.description = request.form['description']
    task.status = request.form['status']
    task.due_date = request.form['due_date']
    task.priority = request.form['priority']
    db.session.commit()
    return redirect(url_for('index'))

# Define the HTML templates
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)