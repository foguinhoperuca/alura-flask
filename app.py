from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from games.views import bp_game
from settings import ALLOWED_HOST, ALLOWED_PORT, DEBUG, SECRET_KEY


# TODO see initialization in __init__.py (turn it into python module)
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from auth.views import bp_auth  # noqa: E402
from games_db.views import bp_games_db  # noqa: E402
app.register_blueprint(bp_game)
app.register_blueprint(bp_games_db, url_prefix='/db')
app.register_blueprint(bp_auth)


@app.route('/home')
def home() -> str:
    return '<h1>Hello World!!</h1>'


@app.route('/')
def index():
    return render_template('menu.html', title="Choose Your Destiny")


print(f'{DEBUG=}')
if __name__ == '__main__':
    if DEBUG:
        app.run(debug=True)
    else:
        app.run(host=ALLOWED_HOST, port=ALLOWED_PORT)
