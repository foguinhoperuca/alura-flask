from functools import wraps

from flask import redirect, session, url_for
from termcolor import colored


def validate_user_logged_in(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(colored('---------- Validate user logged in ----------', 'yellow'))
        if 'user' not in session or session['user'] is None:
            return redirect(url_for('bp_auth.login', next_page=url_for('index')))

        return fn(*args, **kwargs)

    return wrapper
