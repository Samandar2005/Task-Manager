# app.py
from flask import Flask, request, redirect, url_for, render_template
from models import db, Task
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.status = 'completed' if task.status == 'pending' else 'pending'
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/archive')
def archive_tasks():
    completed_tasks = Task.query.filter_by(status='completed').all()
    for task in completed_tasks:
        db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
