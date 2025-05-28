import os
from typing import Dict, List

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, send_file, session, url_for
from termcolor import colored
import weasyprint

from business import Game, GameConsole, GameCategory, get_initial_catalog, get_users, User


load_dotenv()
DEBUG = bool(int(os.getenv('DEBUG', 0)))
ALLOWED_HOST = str(os.getenv('ALLOWED_HOST', 'localhost'))
ALLOWED_PORT = str(os.getenv('ALLOWED_PORT', '8080'))
if DEBUG:
    print(colored(f'{ALLOWED_HOST=} :: {ALLOWED_PORT=}', 'yellow'))

app = Flask(__name__)
app.secret_key = str(os.getenv('SECRET_KEY'))
game_catalog: List[str] = get_initial_catalog()
users: Dict[str, User] = get_users()


@app.route('/home')
def home() -> str:
    return '<h1>Hello World!!</h1>'


@app.route('/')
def index():
    return render_template('menu.html', title="Menu of Options")


@app.route('/list')
def list_games():
    return render_template('list.html', title='My Personal Game List', games=game_catalog)


@app.route('/list_by_console')
def list_by_console():
    return render_template('list_by.html', title="List of Games - Console", games=Game.order_by(games=game_catalog, attr=GameConsole))


@app.route('/list_by_category')
def list_by_category():
    return render_template('list_by.html', title="List of Games - Category", games=Game.order_by(games=game_catalog, attr=GameCategory))


@app.route('/new')
def new():
    if 'user' not in session or session['user'] is None:
        return redirect(url_for('login', next_page=url_for('new')))

    return render_template('new.html', title='New Game Setup', categories=[(e.name, e.value) for e in GameCategory], consoles=[(e.name, e.value) for e in GameConsole])


@app.route('/create', methods=['POST',])
def create():
    name: str = request.form['name']
    category: GameCategory = request.form['category']
    console: GameConsole = request.form['console']

    game_catalog.append(Game(name=name, category=category, console=console))

    return redirect(url_for('list_games'))


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


@app.route('/print')
def print():
    css = weasyprint.CSS('static/print.css')
    html = weasyprint.HTML(string=render_template('list_print.html', title='Printable Game List', games=game_catalog))
    html.write_pdf('/tmp/game_list.pdf', stylesheets=[css])

    return send_file('/tmp/game_list.pdf', download_name='game_list.pdf', mimetype='application/pdf')


app.run(host=ALLOWED_HOST, port=ALLOWED_PORT)
