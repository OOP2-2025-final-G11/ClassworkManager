from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from routes.classwork_dashboard import get_timetable, DAYS, PERIODS, DAY_LABELS

app = Flask(__name__)

# データベースの初期化
initialize_database()

# 各Blueprintをアプリケーションに登録
for blueprint in blueprints:
    app.register_blueprint(blueprint)

# ホームページのルート
@app.route('/')
def index():
    return render_template(
        'index.html',
        timetable=get_timetable(),
        days=DAYS,
        day_labels=DAY_LABELS,
        periods=PERIODS,
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
