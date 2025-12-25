from flask import Blueprint, render_template, request, redirect, url_for

# Blueprint
todo_bp = Blueprint('todo', __name__, url_prefix='/todo')


# =====================
# Todoページ
# =====================
@todo_bp.route('/add')
def todo():
    return render_template('todo_add.html')
