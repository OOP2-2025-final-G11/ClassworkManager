from flask import Blueprint, render_template, request, jsonify
import json
from services.gemini import analyze_with_gemini
from models.classwork import Classwork
from models.db import db

# Blueprint
timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')

UPLOAD_DIR = "uploads"


# =====================
# 時間割スクショアップロードページ（GET）
# =====================
@timetable_bp.route('/upload', methods=['GET'])
def upload_page():
    return render_template('timetable_upload.html')


# =====================
# 時間割スクショアップロード処理（POST）
# =====================
@timetable_bp.route('/upload', methods=['POST'])
def upload_image():
    # 画像が送られてきているか
    if 'image' not in request.files:
        return jsonify({"classworks": []}), 400

    file = request.files['image']

    # ファイル名チェック
    if file.filename == '':
        return jsonify({"classworks": []}), 400
    # ★ ファイルは保存しない（FileStorage を直接渡す）
    result = analyze_with_gemini(file)

    print(json.dumps(result, ensure_ascii=False, indent=2))

    classworks = result.get("classworks", [])

    # ===== DB保存処理 =====
    with db.atomic():
        #既存の授業データを全削除
        Classwork.delete().execute()

        #Geminiから得た授業データを保存
        for cw in classworks:
            Classwork.create(
                name=cw.get("name", ""),
                teacher=cw.get("teacher", ""),
                place=cw.get("place", ""),
                day_of_work=cw.get("day_of_work"),
                period=cw.get("period")
            )

    # 必ず JSON を返す
    return jsonify(result)
