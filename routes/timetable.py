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
        return jsonify({
            "success": False,
            "message": "画像ファイルが見つかりません",
            "classworks": []
        }), 400

    file = request.files['image']

    # ファイル名チェック
    if file.filename == '':
        return jsonify({
            "success": False,
            "message": "画像ファイルが見つかりません",
            "classworks": []
        }), 400
    
    # ★ ファイルは保存しない（FileStorage を直接渡す）
    result = analyze_with_gemini(file)

    classworks = result.get("classworks", [])

    # 授業データが取得できなかった場合
    if not classworks or len(classworks) == 0:
        return jsonify({
            "success": False,
            "message": "時間割の読み取りに失敗しました。別の画像をお試しください。",
            "classworks": []
        }), 200

    # ===== DB保存処理 =====
    try:
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
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "時間割の読み取りに失敗しました。別の画像をお試しください。",
            "classworks": []
        }), 500

    # 成功時のレスポンス
    return jsonify({
        "success": True,
        "message": "時間割を読み取りました",
        "classworks": classworks
    })
