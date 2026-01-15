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

# 課題を完了にする
@todo_bp.route('/complete/<int:todo_id>', methods=['POST'])
def complete(todo_id):
    todo = Todo.get_by_id(todo_id)
    todo.is_finished = not todo.is_finished 
    todo.save() 
    return redirect(url_for('index'))

# 課題を削除する
@todo_bp.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    todo = Todo.get_by_id(todo_id)
    todo.delete_instance()
    return redirect(url_for('index'))

# 完了した課題を一括削除する
@todo_bp.route('/delete_completed', methods=['POST'])
def delete_completed():
    completed_todos = Todo.select().where(Todo.is_finished == True)
    for todo in completed_todos:
        todo.delete_instance()
    return redirect(url_for('index'))