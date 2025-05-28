from functools import wraps

from flask import redirect, session, url_for


def validate_user_logged_in(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print('---------- Validate user logged in ----------')
        if 'user' not in session or session['user'] is None:
            return redirect(url_for('login', next_page=url_for('index')))

        return fn(*args, **kwargs)

    return wrapper
