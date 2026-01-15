from flask import Flask, render_template
from models import initialize_database
from models.todo import Todo
from models.classwork import Classwork
from datetime import datetime, timedelta
from routes.classwork_dashboard import get_timetable, DAYS, PERIODS, DAY_LABELS
import routes
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # 設定
    app.config['SECRET_KEY'] = 'dev-key'

    # データベース初期化
    initialize_database()

    # Blueprint をまとめて登録（遅延取得）
    for blueprint in routes.get_blueprints():
        app.register_blueprint(blueprint)

    # ホームページ
    @app.route('/')
    def index():
        # 課題の完了、削除のために、期限順に並べ替えた課題を取得
        todos = Todo.select().order_by(Todo.is_finished.asc(),Todo.deadline.asc())
        
        return render_template(
            'index.html',
            timetable=get_timetable(),
            days=DAYS,
            day_labels=DAY_LABELS,
            periods=PERIODS,
            todos=todos,
            )
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
