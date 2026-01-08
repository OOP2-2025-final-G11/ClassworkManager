from peewee import Model, CharField, IntegerField
from .db import db

class Subject(Model):
    name = CharField()          # 授業名
    teacher = CharField()       # 教員名
    place = CharField()         # 教室
    day_of_week = CharField()   # MON | TUE | ...
    period = IntegerField()     # 何時限目

    class Meta:
        database = db
