from application.models import *


def get_my_info(js):
    if not is_auth(js):
        raise UserException.BadAuth

    user = User.query.filter_by(login=js.get('verification').get('login'),
                                token=js.get('verification').get('token')).first()

    return user.get_js()


def get_task_list(js):
    if not is_auth(js):
        raise UserException.BadAuth

    user = User.query.filter_by(login=js.get('verification').get('login'),
                                token=js.get('verification').get('token')).first()

    tasks = Task.query.filter(Task.users.any(id=user.id))
    js = {'tasks': []}
    for task in tasks:
        js.get('tasks').append(task.get_js())

    return js


def get_task(js):
    if not is_auth(js):
        raise UserException.BadAuth

    is_owner(js)

    task = Task.query.filter_by(id=js.get('task').get('id')).first()

    return task.get_js()


def add_user(js):
    if not is_auth(js):
        raise UserException.BadAuth

    js_user = js.get('user')
    if not js_user:
        raise UserException.MissedData('Missed user data')

    user = User.new_from_js(js_user)
    db.session.add(user)
    db.session.commit()


def add_task(js):
    if not is_auth(js):
        raise UserException.BadAuth

    js_task = js.get('task')
    if not js_task:
        raise TaskException.MissedData('Missed task data')

    task = Task.new_from_js(js_task)
    user = User.query.filter_by(login=js.get('verification').get('login')).first()
    task.users.append(user)
    db.session.add(task)
    db.session.commit()


def update_user(js):
    if not is_auth(js):
        raise UserException.BadAuth

    js_user = js.get('user')
    if not js_user:
        raise UserException.MissedData('Missed user data')

    user = User.query.filter_by(login=js.get('verification').get('login'),
                                token=js.get('verification').get('token')).first()

    user.update(js.get('user'))
    db.session.commit()


def update_task(js):
    if not is_auth(js):
        raise UserException.BadAuth

    is_owner(js)

    task = Task.query.filter_by(id=js.get('task').get('id')).first()

    task.update(js.get('task'))
    db.session.commit()


def assign_user_to_deal(js):
    if not is_auth(js):
        raise UserException.BadAuth

    is_owner(js)

    if js.get('user') is None or js.get('user').get('login') is None:
        raise UserException.MissedData("Not specified user to assign")

    user = User.query.filter_by(login=js.get('user').get('login')).first()
    if user is None:
        raise UserException.UserNotExists

    task = Task.query.filter_by(id=js.get('task').get('id')).first()
    if user not in task.users:
        task.users.append(user)
        db.session.commit()


def get_user_token(login, password):
    user = User.query.filter_by(login=login, password=password).first()
    if user is None:
        raise UserException.UserNotExists()

    if user.token is None:
        user.set_new_token()
        db.session.commit()

    return user.token, user.login


def is_auth(js):
    verification = js.get('verification')
    if not verification:
        return False

    login = verification.get('login')
    token = verification.get('token')

    if not login or not token:
        return False

    user = User.query.filter_by(login=login, token=token).first()

    return True if user else False


def is_owner(js):
    verification = js.get('verification')
    user = User.query.filter_by(login=verification.get('login'), token=verification.get('token')).first()
    task_js = js.get('task')
    if task_js is None or task_js.get('id') is None:
        raise TaskException.MissedData("No deal for update")
    task = Task.query.filter_by(id=task_js.get('id')).first()
    if task is None:
        raise TaskException.TaskNotExists

    if user not in task.users:
        raise TaskException.DataViolation


def drop_db():
    db.drop_all()
    db.create_all()

    user1 = User(login='admin', password='admin', name='Administrator')
    user2 = User(login='user', password='user', name='User')
    task1 = Task(name='Make task board', description='I should add some extra information', status=Task.Status.TO_DO)
    task2 = Task(name='Check task board', description='I want to see real example', status=Task.Status.IN_PROGRESS)

    task1.users.append(user1)
    task2.users.append(user1)
    task2.users.append(user2)
    db.session.add_all([user1, user2])
    db.session.add_all([task1, task2])

    db.session.commit()
