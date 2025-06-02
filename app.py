import os

from dotenv import load_dotenv
from flask import Flask, render_template
from termcolor import colored

from games.views import bp_game
from auth.views import bp_auth


load_dotenv()
DEBUG = bool(int(os.getenv('DEBUG', 0)))
ALLOWED_HOST: str = str(os.getenv('ALLOWED_HOST', 'localhost'))
ALLOWED_PORT: str = str(os.getenv('ALLOWED_PORT', '8080'))
if DEBUG:
    print(colored(f'{ALLOWED_HOST=} :: {ALLOWED_PORT=}', 'yellow'))


# TODO see initialization in __init__.py
app = Flask(__name__)
app.secret_key = str(os.getenv('SECRET_KEY'))
app.register_blueprint(bp_game)
app.register_blueprint(bp_auth)


@app.route('/home')
def home() -> str:
    return '<h1>Hello World!!</h1>'


@app.route('/')
def index():
    return render_template('menu.html', title="Choose Your Destiny")


if __name__ == '__main__':
    if DEBUG:
        app.run(host=ALLOWED_HOST, port=ALLOWED_PORT)
    else:
        app.run(debug=True)
