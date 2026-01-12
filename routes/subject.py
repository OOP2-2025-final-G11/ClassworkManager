from flask import Blueprint, render_template, request, redirect, url_for
from models.classwork import Classwork

subject_bp = Blueprint('subject', __name__, url_prefix='/subjects')

DAY_LABELS = {
    'MON': '月',
    'TUE': '火',
    'WED': '水',
    'THU': '木',
    'FRI': '金'
}

# 授業一覧
@subject_bp.route('/')
def list():
    subjects = Classwork.select()
    return render_template(
        'subject_list.html',
        title='授業一覧',
        subjects=subjects,
        day_labels=DAY_LABELS
    )


# 授業追加
@subject_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        teacher = request.form['teacher']
        place = request.form['place']
        day_of_work = request.form['day_of_work']
        period = int(request.form['period'])
        force = request.form.get('force')

        # 同じ曜日・時限の授業を検索
        existing = Classwork.get_or_none(
            (Classwork.day_of_work == day_of_work) &
            (Classwork.period == period)
        )

        # 既存授業があり、まだ確認していない場合
        if existing and force != 'yes':
            return render_template(
                'subject_add.html',
                conflict=existing,
                form_data=request.form,
                day_labels=DAY_LABELS
            )

        # 確認済み or 既存授業なし
        if existing:
            existing.delete_instance()

        Classwork.create(
            name=name,
            teacher=teacher,
            place=place,
            day_of_work=day_of_work,
            period=period
        )
        return redirect(url_for('subject.list'))

    return render_template(
        'subject_add.html',
        day_labels=DAY_LABELS
        )


# 授業編集（削除もここで）
@subject_bp.route('/edit/<int:subject_id>', methods=['GET', 'POST'])
def edit(subject_id):
    subject = Classwork.get_or_none(Classwork.id == subject_id)
    if not subject:
        return redirect(url_for('subject.list'))

    if request.method == 'POST':
        if 'delete' in request.form:
            subject.delete_instance()
            return redirect(url_for('subject.list'))

        name = request.form['name']
        teacher = request.form['teacher']
        place = request.form['place']
        day_of_work = request.form['day_of_work']
        period = int(request.form['period'])
        force = request.form.get('force')

        # 自分以外で同じ曜日・時限の授業を検索
        conflict = Classwork.get_or_none(
            (Classwork.day_of_work == day_of_work) &
            (Classwork.period == period) &
            (Classwork.id != subject.id)
        )

        # 衝突あり & 未確認 → ポップアウト用に再描画
        if conflict and force != 'yes':
            return render_template(
                'subject_edit.html',
                subject=subject,
                conflict=conflict,
                form_data=request.form,
                day_labels=DAY_LABELS
            )

        # OKされた場合は既存授業を削除
        if conflict:
            conflict.delete_instance()

        # 編集内容を保存
        subject.name = name
        subject.teacher = teacher
        subject.place = place
        subject.day_of_work = day_of_work
        subject.period = period
        subject.save()

        return redirect(url_for('subject.list'))

    return render_template('subject_edit.html',
                           subject=subject,
                           day_labels=DAY_LABELS
                           )
