from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

from models.todo import Todo
from models.classwork import Classwork

# Blueprint
todo_bp = Blueprint('todo', __name__, url_prefix='/todo')


@todo_bp.route('/add', methods=['GET', 'POST'])
def todo_add():
    classworks = Classwork.select()

    if request.method == 'POST':
        classwork_id = request.form.get('classwork_id')
        name = request.form.get('name')
        deadline_str = request.form.get('deadline')

        deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')

        Todo.create(
            classwork=classwork_id,
            name=name,
            is_finished=False,
            deadline=deadline
        )

        return redirect(url_for('todo.todo_add'))

    return render_template(
        'todo_add.html',
        classworks=classworks
    )
