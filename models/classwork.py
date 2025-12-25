from peewee import Model, CharField, IntegerField
from .db import db

class Classwork(Model):
    name = CharField()  # 授業名
    teacher = CharField()  # 教員名
    place = CharField()  # 教室
    day_of_work = CharField()  # MON | TUE | WED | THU | FRI
    period = IntegerField()  # 時限目

    class Meta:
        database = db