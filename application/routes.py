from application import app
from .exceptions import UserException, TaskException
from flask import render_template, request, abort, make_response, redirect, url_for, jsonify
import application.taskboard as taskboard


@app.errorhandler(401)
def handle_error(error):
    if error.description == 'The server could not verify that you are authorized to access the URL requested. You ' \
                            'either supplied the wrong credentials (e.g. a bad password), or your browser doesn\'t ' \
                            'understand how to supply the credentials required.':
        return "Something went wrong", 401
    return error.description, 401


@app.route('/')
def index():
    abort(401)
    return render_template('index.html')


@app.route('/add_user', methods=['POST'])
def add_user():
    js = request.get_json()
    if not js or type(js) is not dict:
        abort(401)

    print("Data {}".format(request.get_json()))

    try:
        taskboard.add_user(js)
        return 'OK'

    except UserException.Exceptions as e:
        print(e.__str__())
        abort(401, e.__str__())
        return e.__str__(),
    except:
        abort(401)


@app.route('/add_task', methods=['POST'])
def add_task():
    js = request.get_json()
    if not js or type(js) is not dict:
        abort(401)

    print("Data {}".format(request.get_json()))

    try:
        taskboard.add_task(js)
        return 'OK'

    except (UserException.Exceptions, TaskException.Exceptions) as e:
        print(e.__str__())
        abort(401, e.__str__())
        return e.__str__(),
    except:
        abort(401)


@app.route('/update_user', methods=['POST'])
def update_user():
    js = request.get_json()
    if not js or type(js) is not dict:
        abort(401)

    print("Data {}".format(request.get_json()))

    try:
        taskboard.update_user(js)
        return 'OK'

    except UserException.Exceptions as e:
        print(e.__str__())
        abort(401, e.__str__())
        return e.__str__(),
    except:
        abort(401)


@app.route('/assign_user_to_task', methods=['POST'])
def assign_user_to_task():
    js = request.get_json()
    if not js or type(js) is not dict:
        abort(401)

    print("Data {}".format(request.get_json()))

    try:
        taskboard.assign_user_to_deal(js)
        return 'OK'

    except (TaskException.Exceptions, UserException.Exceptions) as e:
        print(e.__str__())
        abort(401, e.__str__())
        return e.__str__(),
    except:
        abort(401)


@app.route('/update_task', methods=['POST'])
def update_task():
    js = request.get_json()
    if not js or type(js) is not dict:
        abort(401)

    print("Data {}".format(request.get_json()))

    try:
        taskboard.update_task(js)
        return 'OK'

    except (UserException.Exceptions, TaskException.Exceptions) as e:
        print(e.__str__())
        abort(401, e.__str__())
        return e.__str__(),
    except Exception as e:
        print(e.__str__())
        abort(401)


@app.route('/task_list', methods=['POST'])
def get_task_list():
    js = request.get_json()
    if not js or type(js) is not dict:
        abort(401)
    try:
        js = taskboard.get_task_list(js)
        return jsonify(js)
    except (UserException.Exceptions, TaskException.Exceptions) as e:
        abort(401, e.__str__())
    except:
        abort(401)


@app.route('/get_task', methods=['POST'])
def get_task():
    js = request.get_json()
    if not js or type(js) is not dict:
        abort(401)

    try:
        js = taskboard.get_task(js)
        return jsonify(js)
    except (UserException.Exceptions, TaskException.Exceptions) as e:
        abort(401, e.__str__())
    except:
        abort(401)


@app.route('/me', methods=['POST'])
def get_me():
    js = request.get_json()
    if not js or type(js) is not dict:
        abort(401)
    try:
        js = taskboard.get_my_info(js)
        return jsonify(js)
    except UserException.Exceptions as e:
        abort(401, e.__str__())
    except:
        abort(401)


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    redir = request.args.get('redirect')
    if redir is None:
        return "No redirect param"

    error = None
    if request.method == 'POST':
        token = login = None
        try:
            token, login = taskboard.get_user_token(login=request.form['login'], password=request.form['password'])
        except UserException.Exceptions as e:
            error = e.__str__()

        if token is not None:
            return redirect("{}?token={}&login={}".format(redir, token, login))
    return render_template('login.html', error=error)


@app.route('/resetDB')
def reset_db():
    taskboard.drop_db()
    return render_template('index.html')
