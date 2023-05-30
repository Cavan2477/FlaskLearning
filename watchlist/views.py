from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user

from watchlist.models import Movie, User
from watchlist import app, db


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):  # put application's code here
    return render_template('hello.html', name=name)


@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    # 判断请求
    if request.method == 'POST':
        # 判定用户是否已认证
        if not current_user.is_authenticated:
            return redirect(url_for('index'))

        # 获取表单数据
        title = request.form.get('title')
        year = request.form.get('year')

        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))

        # 创建记录
        movie = Movie(title=title, year=year)

        db.session.add(movie)
        db.session.commit()

        flash('Item created')

        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title
        movie.year = year

        db.session.commit()

        flash('Item updated.')

        return redirect(url_for('index'))

    # 传入被编辑过的电影记录
    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    db.session.delete(movie)
    db.session.commit()

    flash('Item delete.')

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')

            return redirect(url_for('login'))

        user = User.query.first()

        # 验证用户名与密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)

            flash('Login success.')

            return redirect(url_for('index'))

        flash('Invalid username or password.')
        return redirect(url_for('login'))

    return render_template('login.html')


# 用户登出
@app.route('/logout')
@login_required
def logout():
    logout_user()

    flash('Goodbye.')

    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()

        flash('Settings updated.')

        return redirect(url_for('index'))

    return render_template('settings.html')


# @app.route('/user/<name>')
# def user_page(name):
#     return f'User: {escape(name)}'
#
#
# @app.route('/test')
# def test_url_for():
#     print(url_for('hello'))
#     print(url_for('user_page', name='CavanLiu'))
#     print(url_for('user_page', name='Cavan'))
#     print(url_for('test_url_for'))
#     print(url_for('test_url_for', num=2))
#     return 'Test Page'