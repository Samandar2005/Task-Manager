from flask import Flask, request, redirect, url_for, render_template, flash
from models import db, Task, User
from config import Config
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import secrets

secret_key = secrets.token_hex(32)

app = Flask(__name__)
app.secret_key = secret_key
app.config.from_object(Config)
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('signup'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! You can now log in.')
        return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))

        flash('Invalid username or password!')

    return render_template('login.html')


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
@login_required
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    new_task = Task(title=title, description=description, user_id=current_user.id)  # Set user_id to current user
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))



@app.route('/delete/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:  # Only delete if task belongs to the current user
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    task = Task.query.get(task_id)
    if task and task.user_id == current_user.id:  # Only update if task belongs to the current user
        task.status = 'completed' if task.status == 'pending' else 'pending'
        db.session.commit()
    return redirect(url_for('index'))


@app.route('/archive')
@login_required
def archive_tasks():
    completed_tasks = Task.query.filter_by(status='completed').all()
    for task in completed_tasks:
        db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
