from flask import Blueprint, render_template, request, jsonify
import os
from services.gemini import analyze_with_gemini
import json

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

    # 必ず JSON を返す
    return jsonify(result)
