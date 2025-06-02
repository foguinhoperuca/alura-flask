from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from auth.views import bp_auth
from games.views import bp_game
from games_db.views import bp_game_db
from settings import ALLOWED_HOST, ALLOWED_PORT, DEBUG, SECRET_KEY


# TODO see initialization in __init__.py
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config.from_pyfile('settings.py')

app.register_blueprint(bp_game)
app.register_blueprint(bp_game_db, url_prefix='/db')
app.register_blueprint(bp_auth)

db = SQLAlchemy(app)


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
