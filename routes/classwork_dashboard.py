from flask import Blueprint
from models.classwork import Classwork

classwork_bp = Blueprint("classwork", __name__)

DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
DAY_LABELS = {
    "MON": "月",
    "TUE": "火",
    "WED": "水",
    "THU": "木",
    "FRI": "金",
}
PERIODS = 5

def get_timetable():
    table = {
        day: [None] * PERIODS for day in DAYS
    }

    # DBから取得する
    for cw in Classwork.select():
        table[cw.day_of_work][cw.period - 1] = cw

    return table