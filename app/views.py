from flask import render_template, redirect, url_for, flash
from app import app, db
from datetime import datetime
from app.models import Task
from app.forms import TaskForm

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
