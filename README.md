# Watchlist

Demo: https://CodeCaptain.pythonanywhere.com

## Installation

clone:
```
$ git clone https://github.com/Cavan2477/FlaskLearning.git
$ cd FlaskLearning
```
create & active virtual enviroment then install dependencies:
```
$ python3 -m venv env  # use `python ...` on Windows
$ source env/bin/activate  # use `env\Scripts\activate` on Windows

pipenv is not installed
install dependencies
(env) $ pip install -r requirements.txt

pipenv is installed
$ pip install pipenv
$ pipenv shell
$ pipenv install alembic blinker click colorama coverage Flask Flask-Login Flask-Migrate Flask-SQLAlchemy greenlet itsdangerous Jinja2 Mako MarkupSafe python-dot
env SQLAlchemy typing_extensions werkzeug
$ pipenv install watchdog --dev
```

Account information:
```
account: admin
pwd: 111111
```

generate fake data then run:
```
(env) $ flask forge
(env) $ flask admin
(env) $ flask run

* Running on http://127.0.0.1:5000/
* Login by admin/111111
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
