import os
from typing import List

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, session, url_for
from termcolor import colored

from business import Game, GameConsole, GameCategory, get_initial_catalog


load_dotenv()
DEBUG = bool(int(os.getenv('DEBUG', 0)))
ALLOWED_HOST = str(os.getenv('ALLOWED_HOST', 'localhost'))
ALLOWED_PORT = str(os.getenv('ALLOWED_PORT', '8080'))
if DEBUG:
    print(colored(f'{ALLOWED_HOST=} :: {ALLOWED_PORT=}', 'yellow'))

app = Flask(__name__)
game_catalog: List[str] = get_initial_catalog()


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
    return render_template('new.html', title='New Game Setup')


@app.route('/create', methods=['POST',])
def create():
    name: str = request.form['name']
    category: GameCategory = request.form['category']
    console: GameConsole = request.form['console']

    game_catalog.append(Game(name=name, category=category, console=console))

    return redirect(url_for('list_games'))


app.run(host=ALLOWED_HOST, port=ALLOWED_PORT)
