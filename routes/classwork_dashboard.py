from flask import Blueprint
from models.classwork import Classwork

classwork_bp = Blueprint("classwork", __name__)

DAYS = ["MON", "TUE", "WED", "THU", "FRI"]
PERIODS = 5

def get_timetable():
    table = {
        day: [None] * PERIODS for day in DAYS
    }

    # DBから取得する場合
    # for cw in Classwork.select():
    #     table[cw.day_of_work][cw.period - 1] = cw

    return table