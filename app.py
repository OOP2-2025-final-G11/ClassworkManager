from flask import Flask, render_template
from models import initialize_database
from routes import blueprints
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    # 設定
    app.config['SECRET_KEY'] = 'dev-key'

    # データベース初期化
    initialize_database()

    # Blueprint をまとめて登録
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # ホームページ
    @app.route('/')
    def index():
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
