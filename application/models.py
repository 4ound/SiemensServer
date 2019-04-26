from flask_sqlalchemy import SQLAlchemy
from enum import Enum
from .exceptions import UserException, TaskException
from hashlib import md5
from os import urandom

db = SQLAlchemy()

tags = db.Table('user_task',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True)
                )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(32, collation='utf8mb4_0900_as_cs'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    token = db.Column(db.String(128, collation='utf8mb4_0900_as_cs'), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.login

    def update(self, js):
        login = js.get('login')
        if login is not None:
            if self.login != login and not User._check_login_existance(login):
                raise UserException.UserExists
            self.login = login

        password = js.get('password')
        if password is not None:
            self.password = password

        name = js.get('name')
        if name is not None:
            self.name = name

        token = js.get('token')
        if token is not None:
            self.set_new_token()

    def set_new_token(self):
        self.token = md5(urandom(32)).hexdigest()

    def new_from_js(js):
        login = js.get('login')
        password = js.get('password')
        name = js.get('name')

        if not User._check_login_existance(login):
            raise UserException.UserExists

        return User(login=login, password=password, name=name)

    def _check_login(login):
        return True

    def _check_password(password):
        return True

    def _check_name(name):
        return True

    def _check_login_existance(login):
        user = User.query.filter_by(login=login).first()
        return True if user is None else False

    def _check_user_correct_by_pswd(login, password):
        user = User.query.filter_by(login=login, password=password).first()
        return False if user is None else False

    def _check_user_correct_by_token(login, token):
        user = User.query.filter_by(login=login, token=token).first()
        return False if user is None else False

    def get_js(self):
        return {
            "login": self.login,
            "name": self.name,
        }


class Task(db.Model):
    class Status(Enum):
        TO_DO = 'TO_DO'
        IN_PROGRESS = 'IN_PROGRESS'
        ON_REVIEW = 'ON_REVIEW'
        DONE = 'DONE'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(2048), nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    users = db.relationship('User', secondary=tags, lazy='subquery',
                            backref=db.backref('task', lazy=True))

    def get_js(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'status': self.status.value,
            'users': [user.get_js() for user in self.users]
        }

    def update(self, js):
        name = js.get('name')
        if name is not None:
            self.name = name

        description = js.get('description')
        if description is not None:
            self.description = description

        status = js.get('status')
        if status is not None:
            try:
                status = Task.Status(status)
            except:
                raise TaskException.WrongStatus
            self.status = status

    def new_from_js(js):
        name = js.get('name')
        description = js.get('description')
        status = js.get('status')
        try:
            status = Task.Status(status)
        except:
            raise TaskException.WrongStatus

        return Task(name=name, description=description, status=status)
