from flask import render_template, redirect, url_for, flash,request
from app.models import Task, User,Tag
from app.forms import TaskForm
from app import app, db, admin
from flask_admin.contrib.sqla import ModelView
from app.forms import RegistrationForm, LoginForm, BlogPostForm, DeleteForm
from flask_login import login_user, logout_user, login_required, current_user

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Tag, db.session))

# View all tasks
@app.route('/')
@app.route('/tasks')
def index():
    in_progress = Task.query.filter_by(status=False).all()
    completed = Task.query.filter_by(status=True).all()
    return render_template('todo_list.html', in_progress=in_progress, completed=completed, filter='All Tasks')

# Add new task
@app.route('/add', methods=['GET', 'POST'])
def add():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(
            assessment_title=form.assessment_title.data,
            module_code=form.module_code.data,
            deadline_date=form.deadline_date.data,
            description=form.description.data,
            status=False
        )
        db.session.add(new_task)
        db.session.commit()
        flash('New task added successfully!')
        return redirect(url_for('todo_list'))
    else:
        print(form.errors)
    return render_template('todo_list.html', form=form)

# Edit an assessment
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    form = Task(obj=task)
    if form.validate_on_submit():
        task.assessment_title = form.assessment_title.data
        task.module_code = form.module_code.data
        task.deadline_date = form.deadline_date.data
        task.description = form.description.data
        task.status = form.status.data
        db.session.commit()
        flash('Task updated successfully!')
        return redirect(url_for('todo_list'))
    return render_template('todo_list.html', form=form, task=task)

# See all the details for the assessment
@app.route('/view/<int:id>')
def view(id):
    task = Task.query.get_or_404(id)
    return render_template('todo_list.html', task=task)

# Mark task's status
@app.route('/toggle_status/<int:id>')
def toggle_status(id):
    task = Task.query.get_or_404(id)
    task.status = not task.status
    db.session.commit()
    flash('Task status updated successfully!')
    return redirect(url_for('todo_list'))

# View uncompleted tasks
@app.route('/uncomplete')
def uncomplete():
    in_progress = Task.query.filter_by(status=False).all()
    return render_template('todo_list.html', in_progress=in_progress, filter='Uncompleted Tasks')

# View completed tasks
@app.route('/completed')
def completed():
    completed = Task.query.filter_by(status=True).all()
    return render_template('todo_list.html', completed=completed, filter='Completed Tasks')

# Delete an task
@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!')
    return redirect(url_for('todo_list'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You have already logged in')
        form = LoginForm()
        return render_template('login.html', form=form, already_logged_in=True) 
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid email or password')
                return redirect(url_for('login'))
            login_user(user)
            flash('Welcome back, {}'.format(user.username))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        return render_template('login.html', form=form)

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
            flash('Congratulations, you have successfully registered!')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering. Please try again.')
    return render_template('register.html', form=form)
