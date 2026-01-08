from flask import Blueprint, render_template, request, redirect, url_for
from models.todo import Todo 

# Blueprint
todo_bp = Blueprint('todo', __name__, url_prefix='/todo')


# =====================
# Todoページ
# =====================
@todo_bp.route('/add')
def todo():
    return render_template('todo_add.html')



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