#グラフで登録日時が欲しい
from peewee import Model, CharField, DateTimeField, ForeignKeyField, BooleanField
from datetime import datetime
from .db import db
from .classwork import Classwork

class Todo(Model):
    classwork = ForeignKeyField(Classwork, backref='todos', column_name='classwork_id') # この課題の授業
    name = CharField() # 課題内容
    is_finished = BooleanField(default=False) # デフォルトで未完了
    deadline = DateTimeField() # 期限

    class Meta:
        database = db
