from typing import Dict

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from auth.models import get_users, User, UsersDB


bp_auth = Blueprint('bp_auth', __name__, template_folder='templates', static_folder='static')
users: Dict[str, User] = get_users()


@bp_auth.route('/login')
def login():
    assert request.args.get('next_page')
    return render_template('user/login.html', next_page=request.args.get('next_page'))


@bp_auth.route('/logout')
def logout():
    session['user'] = None
    flash('Logout was successfully', 'info')

    return redirect(url_for('index'))


@bp_auth.route('/authentication', methods=['POST',])
def authentication():
    if request.form['username'] in users:
        user: User = users[request.form['username']]
        if user.authenticate(username=request.form['username'], password=request.form['password']):
            session['user'] = user.username
            flash(f'[MEM] {user} was successfully logged!!', 'success')

            return redirect(request.form['next_page'])
        else:
            session['user'] = None
            flash(f'[MEM] {user} failed to login!!', 'danger')

            return redirect(url_for('bp_auth.login', next_page=request.form['next_page']))

    else:
        user_db: UsersDB = UsersDB.query.filter_by(username=request.form['username']).first()
        if user_db:
            if user_db.authenticate(username=request.form['username'], password=request.form['password']):
                session['user'] = user_db.username
                flash(f'[DB] {user_db} was successfully logged!!', 'primary')

                return redirect(request.form['next_page'])
            else:
                session['user'] = None
                flash(f'[DB] {user_db} failed to login!!', 'secondary')

                return redirect(url_for('bp_auth.login', next_page=request.form['next_page']))

        session['user'] = None
        flash(f'{request.form["username"]} User not available!!', 'warning')
        return redirect(url_for('bp_auth.login', next_page=request.form['next_page']))
