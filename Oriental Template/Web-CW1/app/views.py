from flask import render_template, redirect, url_for, flash
from app import app, db
from datetime import datetime
from app.models import Assessment
from app.forms import AssessmentForm

# View all assessments
@app.route('/')
@app.route('/assessments')
def index():
    in_progress = Assessment.query.filter_by(status=False).all()
    completed = Assessment.query.filter_by(status=True).all()
    return render_template('index.html', in_progress=in_progress, completed=completed, filter='All Assessments')

# Add new assessment
@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AssessmentForm()
    if form.validate_on_submit():
        new_assessment = Assessment(
            assessment_title=form.assessment_title.data,
            module_code=form.module_code.data,
            deadline_date=form.deadline_date.data,
            description=form.description.data,
            status=False
        )
        db.session.add(new_assessment)
        db.session.commit()
        flash('New assessment added successfully!')
        return redirect(url_for('index'))
    else:
        print(form.errors)
    return render_template('add.html', form=form)

# Edit an assessment
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    assessment = Assessment.query.get_or_404(id)
    form = AssessmentForm(obj=assessment)
    if form.validate_on_submit():
        assessment.assessment_title = form.assessment_title.data
        assessment.module_code = form.module_code.data
        assessment.deadline_date = form.deadline_date.data
        assessment.description = form.description.data
        assessment.status = form.status.data
        db.session.commit()
        flash('Assessment updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', form=form, assessment=assessment)

# See all the details for the assessment
@app.route('/view/<int:id>')
def view(id):
    assessment = Assessment.query.get_or_404(id)
    return render_template('view.html', assessment=assessment)

# Mark assessment's ststus
@app.route('/toggle_status/<int:id>')
def toggle_status(id):
    assessment = Assessment.query.get_or_404(id)
    assessment.status = not assessment.status
    db.session.commit()
    flash('Assessment status updated successfully!')
    return redirect(url_for('index'))

# View uncompleted assessments
@app.route('/uncomplete')
def uncomplete():
    in_progress = Assessment.query.filter_by(status=False).all()
    return render_template('index.html', in_progress=in_progress, filter='Uncompleted Assessments')

# View completed assessments
@app.route('/completed')
def completed():
    completed = Assessment.query.filter_by(status=True).all()
    return render_template('index.html', completed=completed, filter='Completed Assessments')

# Delete an assessment
@app.route('/delete/<int:id>')
def delete(id):
    assessment = Assessment.query.get_or_404(id)
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully!')
    return redirect(url_for('index'))
