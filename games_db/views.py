from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for

from .models import GamesDB
from helper import GameCategory, GameConsole

from helper import validate_user_logged_in


bp_games_db = Blueprint('bp_games_db', __name__, template_folder='templates', static_folder='static')


@bp_games_db.route('/list/')
def list():
    games = GamesDB.query.order_by(GamesDB.id)
    return render_template('games_db/list.html', title='[DB] My Personal Game List', games=games)


@bp_games_db.route('/new')
@validate_user_logged_in
def new():
    return render_template('games_db/new.html', title='My Personal Game List - Database Version', categories=[(e.name, e.value) for e in GameCategory], consoles=[(e.name, e.value) for e in GameConsole])


@bp_games_db.route('/create', methods=['POST',])
@validate_user_logged_in
def create():
    name: str = request.form['name']
    # TODO validate category and console
    category: GameCategory = GameCategory(request.form['category'])
    console: GameConsole = GameConsole(request.form['console'])

    game: GamesDB = GamesDB(name=name, category=category.value, console=console.value)
    print(f'GamesDB is {game}')
    if GamesDB.save(game=game):
        flash(f'Game {game} was successfully saved!', 'success')
    else:
        flash(f'Game {game.name} in console {game.console} already exist! No duplication, please.', 'danger')

    return redirect(url_for('bp_games_db.list'))


@bp_games_db.route('/edit/<int:id>')
@validate_user_logged_in
def edit(id: int):
    game: GamesDB = GamesDB.query.filter_by(id=id).first()
    if game is None:
        flash(f'Game id {id} not found. Make sure that id is correct!', 'danger')
        return redirect(url_for('bp_games_db.list'))

    return render_template('games_db/edit.html', title='Edit Game', game=game, categories=[(e.name, e.value) for e in GameCategory], consoles=[(e.name, e.value) for e in GameConsole])


@bp_games_db.route('/update/<int:id>', methods=['POST',])
@validate_user_logged_in
def update(id: int):
    game: GamesDB = GamesDB.query.filter_by(id=id).first()
    if game is None:
        flash(f'Game id {id} not found. Make sure that id is correct!', 'danger')
    else:
        name: str = request.form['name']
        category: GameCategory = GameCategory(request.form['category'])
        console: GameConsole = GameConsole(request.form['console'])

        game.name = name
        game.category = category
        game.console = console
        if GamesDB.update(game=game):
            flash(f'Game {game} successfully updated!!', 'success')
        else:
            flash(f'Can\'t update game {game} !!', 'danger')

    return redirect(url_for('bp_games_db.list'))


@bp_games_db.route('/delete/<int:id>')
@validate_user_logged_in
def delete(id: int):
    GamesDB.delete(id=id)
    flash('Game was deleted successfuly!', 'success')

    return redirect(url_for('bp_games_db.list'))
