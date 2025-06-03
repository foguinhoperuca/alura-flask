from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy


# TODO should separate db from app?!

def get_db(app):
    if 'db' not in g:
        g.db = SQLAlchemy(app)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
