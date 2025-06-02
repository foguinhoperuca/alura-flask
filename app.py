import os
from typing import Dict

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from termcolor import colored

from business import get_users, User
from games.views import bp_game


load_dotenv()
DEBUG = bool(int(os.getenv('DEBUG', 0)))
ALLOWED_HOST: str = str(os.getenv('ALLOWED_HOST', 'localhost'))
ALLOWED_PORT: str = str(os.getenv('ALLOWED_PORT', '8080'))
DB_ENGINE: str = str(os.getenv('DB_ENGINE', 'memory'))
if DEBUG:
    print(colored(f'{ALLOWED_HOST=} :: {ALLOWED_PORT=}', 'yellow'))


# TODO use blueprint and see initialization in __init__.py
app = Flask(__name__)
app.secret_key = str(os.getenv('SECRET_KEY'))
app.register_blueprint(bp_game)
users: Dict[str, User] = get_users()


@app.route('/home')
def home() -> str:
    return '<h1>Hello World!!</h1>'


@app.route('/')
def index():
    return render_template('menu.html', title="Menu of Options")


@app.route('/login')
def login():
    assert request.args.get('next_page')
    return render_template('user/login.html', next_page=request.args.get('next_page'))


@app.route('/logout')
def logout():
    session['user'] = None
    flash('Logout was successfully', 'info')

    return redirect(url_for('index'))


@app.route('/authentication', methods=['POST',])
def authentication():
    if request.form['username'] in users:
        user: User = users[request.form['username']]
        if user.authenticate(username=request.form['username'], password=request.form['password']):
            session['user'] = user.username
            flash(f'{user} was successfully logged!!', 'success')

            return redirect(request.form['next_page'])
        else:
            session['user'] = None
            flash(f'{user} failed to login!!', 'danger')

            return redirect(url_for('login', next_page=request.form['next_page']))

    else:
        session['user'] = None
        flash(f'{request.form["username"]} User not available!!', 'warning')

        return redirect(url_for('login', next_page=request.form['next_page']))


if __name__ == '__main__':
    if DEBUG:
        app.run(host=ALLOWED_HOST, port=ALLOWED_PORT)
    else:
        app.run(debug=True)
