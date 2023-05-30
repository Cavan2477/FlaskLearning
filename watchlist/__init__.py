import os
import sys

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),
                                                              os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)
migrate = Migrate(app, db)  # 在db对象创建后调用
login_manager = LoginManager(app)

# 登录视图端点（函数名对应）
login_manager.login_view = 'login'


# 创建用户加载回调函数，接受用户 ID 作为参数
@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


# 对于多个模板内都需要使用的变量，我们可以使用 app.context_processor 装饰器注册一个模板上下文处理函数
@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()

    # 需要返回字典，等同于 return {'user': user}
    return dict(user=user)


if __name__ == '__main__':
    app.run()

from watchlist import views, errors, commands
