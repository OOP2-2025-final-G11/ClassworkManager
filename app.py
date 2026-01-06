from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from models.todo import Todo
from models.classwork import Classwork
from datetime import datetime, timedelta

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    # 課題の完了、削除のために、期限順に並べ替えた課題を取得
    todos = Todo.select().order_by(Todo.deadline.asc())
    return render_template('index.html', todos=todos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
