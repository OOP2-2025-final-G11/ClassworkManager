from flask import Blueprint, render_template

# Blueprint
timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')


# =====================
# 時間割スクショアップロードページ
# =====================
@timetable_bp.route('/upload')
def todo():
    return render_template('timetable_upload.html')
