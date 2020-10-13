import asyncio
from _datetime import datetime

from peewee import *
from peewee import Model
import peewee_async

from werkzeug.security import check_password_hash,generate_password_hash

# 数据库连接
db = peewee_async.MySQLDatabase("tornado", host="127.0.0.1", port=3306, user="root", password="qwer1234")
objects = peewee_async.Manager(db)
db.set_allow_sync(False)

# 基类
class BaseModel(Model):
    create_time = DateTimeField(default=datetime.now ,verbose_name="创建时间")

    class Meta:
        database = db


class User(BaseModel):
    username = CharField(max_length=50, verbose_name="姓名", index=True)
    _password = CharField(column_name='password', max_length=50, verbose_name="密码")
    login_time = CharField(max_length=20, verbose_name='登录时间')

    class Meta:
        table_name = "user"

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pwd):
        self._password = generate_password_hash(pwd)

    def check_pwd(self, pwd):
        return check_password_hash(self.password, pwd)



def init_table():
    db.set_allow_sync(True)
    db.create_tables([User], safe=True)



if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(init_table())
    init_table()