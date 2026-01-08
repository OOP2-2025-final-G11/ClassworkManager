from flask import Blueprint, render_template, request, redirect, url_for
from models.classwork import Classwork

subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')


# 授業一覧
@subject_bp.route('/')
def list():
    subjects = Classwork.select()
    return render_template(
        'subject_list.html',
        title='授業一覧',
        subjects=subjects
    )


# 授業追加
@subject_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        Classwork.create(
            name=request.form['name'],
            teacher=request.form['teacher'],
            place=request.form['place'],
            day_of_work=request.form['day_of_work'],
            period=request.form['period']
        )
        return redirect(url_for('subject.list'))

    return render_template('subject_add.html')


# 授業編集（削除もここで）
@subject_bp.route('/edit/<int:subject_id>', methods=['GET', 'POST'])
def edit(subject_id):
    subject = Classwork.get_or_none(Classwork.id == subject_id)
    if not subject:
        return redirect(url_for('subject.list'))

    if request.method == 'POST':
        if 'delete' in request.form:
            subject.delete_instance()
            return redirect(url_for('subject.list'))

        subject.name = request.form['name']
        subject.teacher = request.form['teacher']
        subject.place = request.form['place']
        subject.day_of_work = request.form['day_of_work']
        subject.period = request.form['period']
        subject.save()

        return redirect(url_for('subject.list'))

    return render_template('subject_edit.html', subject=subject)
