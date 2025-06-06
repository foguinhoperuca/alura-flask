from flask import Blueprint, flash, redirect, render_template, request, send_from_directory, url_for

from helper import GameCategory, GameConsole
from settings import UPLOAD_PATH
from .forms import GamesDBForm
from .models import GamesDB

from helper import validate_user_logged_in


bp_games_db = Blueprint('bp_games_db', __name__, template_folder='templates', static_folder='static')


@bp_games_db.route('/games_dbs')
def index():
    games = GamesDB.query.order_by(GamesDB.id)
    return render_template('games_db/index.html', title='[DB] My Personal Game List', games=games)


@bp_games_db.route('/new')
@validate_user_logged_in
def new():
    cover: str = 'cover_generic.jpg'
    form: GamesDBForm = GamesDBForm()
    return render_template('games_db/new.html', title='My Personal Game List - Database Version', cover=cover, form=form, categories=[(e.name, e.value) for e in GameCategory], consoles=[(e.name, e.value) for e in GameConsole])


@bp_games_db.route('/create', methods=['POST',])
@validate_user_logged_in
def create():
    form = GamesDBForm(request.form)
    if not form.validate_on_submit():
        flash('Game invalid! Please, fix it!!', 'danger')
        for key in form.errors.keys():
            for error in form.errors[key]:
                flash(f'[{key}] error: {error}', 'warning')

        return redirect(url_for('bp_games_db.new'))

    name: str = form.name.data
    # TODO validate category and console
    category: GameCategory = GameCategory(request.form['category'])
    console: GameConsole = GameConsole(request.form['console'])

    game: GamesDB = GamesDB(name=name, category=category.value, console=console.value)
    if GamesDB.save(game=game):
        flash(f'Game {game} was successfully saved!', 'success')
        file_uploaded = request.files['cover']
        file_uploaded.save(f'{UPLOAD_PATH}/cover_{game.id}.jpg')
    else:
        flash(f'Game {game.name} in console {game.console} already exist! No duplication, please.', 'danger')

    return redirect(url_for('bp_games_db.index'))


@bp_games_db.route('/show/<int:id>')
def show(id: int):
    game: GamesDB = GamesDB.show(id=id)
    cover: str = f'cover_{game.id}.jpg'

    return render_template('games_db/show.html', title='Show GamesDB Detail', game=game, cover=cover)


@bp_games_db.route('/edit/<int:id>')
@validate_user_logged_in
def edit(id: int):
    game: GamesDB = GamesDB.query.filter_by(id=id).first()
    if game is None:
        flash(f'Game id {id} not found. Make sure that id is correct!', 'danger')
        return redirect(url_for('bp_games_db.index'))

    form: GamesDBForm = GamesDBForm()
    cover: str = f'cover_{game.id}.jpg'

    return render_template('games_db/edit.html', title='Edit Game', game=game, form=form, cover=cover, categories=[(e.name, e.value) for e in GameCategory], consoles=[(e.name, e.value) for e in GameConsole])


@bp_games_db.route('/update/<int:id>', methods=['POST',])
@validate_user_logged_in
def update(id: int):
    game: GamesDB = GamesDB.query.filter_by(id=id).first()
    form = GamesDBForm(request.form)
    if not form.validate_on_submit():
        flash('Game invalid! Please, fix it!!', 'danger')
        for key in form.errors.keys():
            for error in form.errors[key]:
                flash(f'[{key}] error: {error}', 'warning')

        return redirect(url_for('bp_games_db.new'))

    if game is None:
        flash(f'Game id {id} not found. Make sure that id is correct!', 'danger')
    else:
        game.name = form.name.data
        game.category = GameCategory(request.form['category'])
        game.console = GameConsole(request.form['console'])
        if GamesDB.update(game=game):
            flash(f'Game {game} successfully updated!!', 'success')
            file_uploaded = request.files['cover']
            file_uploaded.save(f'{UPLOAD_PATH}/cover_{game.id}.jpg')
        else:
            flash(f'Can\'t update game {game} !!', 'danger')

    return redirect(url_for('bp_games_db.index'))


@bp_games_db.route('/destroy/<int:id>')
@validate_user_logged_in
def destroy(id: int):
    GamesDB.delete(id=id)
    flash('Game was deleted successfuly!', 'success')

    return redirect(url_for('bp_games_db.index'))


@bp_games_db.route(f'{UPLOAD_PATH}/<file_name>')
@validate_user_logged_in
def cover(file_name: str):
    return send_from_directory(f'{UPLOAD_PATH}', file_name)
