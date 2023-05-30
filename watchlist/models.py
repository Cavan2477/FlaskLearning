# 表明将会是user（自动生成，小写处理）
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from watchlist import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password = db.Column(db.String(255))

    # 用来设置密码的方法，接受密码作为参数
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # 用于验证密码的方法，接受密码作为参数
    def validate_password(self, password):
        return check_password_hash(self.password, password)


# 表名将会是 movie
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
