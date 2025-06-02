import os
from typing import Set

from flask import Blueprint, flash, redirect, render_template, request, send_file, url_for
import weasyprint

from .models import Game, GameConsole, GameCategory, get_initial_catalog

# FIXME use import sys bellow to workarround import of helper bellow
# import sys
# sys.path.append('..')
from helper import validate_user_logged_in


DB_ENGINE: str = str(os.getenv('DB_ENGINE', 'memory'))
bp_game = Blueprint('bp_game', __name__, template_folder='templates', static_folder='static')
game_catalog: Set[str] = get_initial_catalog()


@bp_game.route('/list/')
@bp_game.route('/list/<format>')
def list(format: str = None):
    if format == 'console':
        return render_template('games/list_by.html', title="List of Games - Console", games=Game.order_by(games=game_catalog, attr=GameConsole))
    elif format == 'category':
        return render_template('games/list_by.html', title="List of Games - Category", games=Game.order_by(games=game_catalog, attr=GameCategory))
    elif format == 'print':
        css = weasyprint.CSS('static/print.css')
        html = weasyprint.HTML(string=render_template('games/list_print.html', title='Printable Game List', games=game_catalog))
        html.write_pdf('/tmp/game_list.pdf', stylesheets=[css])

        return send_file('/tmp/game_list.pdf', download_name='game_list.pdf', mimetype='application/pdf')

    return render_template('games/list.html', title='My Personal Game List', games=game_catalog)


@bp_game.route('/new')
@validate_user_logged_in
def new():
    return render_template('games/new.html', title='New Game Setup', categories=[(e.name, e.value) for e in GameCategory], consoles=[(e.name, e.value) for e in GameConsole])


@bp_game.route('/create', methods=['POST',])
@validate_user_logged_in
def create():
    name: str = request.form['name']
    # TODO validate category and console
    category: GameCategory = GameCategory(request.form['category'])
    console: GameConsole = GameConsole(request.form['console'])
    game: Game = Game(name=name, category=category, console=console)
    game_catalog.add(game)
    flash(f'Game {game} was successfully saved!', 'success')

    return redirect(url_for('bp_game.list_games'))


@bp_game.route('/edit/<int:id>')
@validate_user_logged_in
def edit(id: int):
    game: Game = Game.find_game_in_catalog(id=id, catalog=game_catalog)
    if game is None:
        flash(f'Game id {id} not found. Make sure that id is correct!', 'error')
        return redirect(url_for('bp_game.list_games'))

    return render_template('games/edit.html', title='Edit Game', game=game, categories=[(e.name, e.value) for e in GameCategory], consoles=[(e.name, e.value) for e in GameConsole])


@bp_game.route('/update/<int:id>', methods=['POST',])
@validate_user_logged_in
def update(id: int):
    game: Game = Game.find_game_in_catalog(id=id, catalog=game_catalog)
    if game is None:
        flash(f'Game id {id} not found. Make sure that id is correct!', 'error')
    else:
        name: str = request.form['name']
        # TODO validate category and console
        category: GameCategory = GameCategory(request.form['category'])
        console: GameConsole = GameConsole(request.form['console'])

        game.name = name
        game.category = category
        game.console = console

        flash(f'Game {game} successfully updated!!', 'success')

    return redirect(url_for('bp_game.list_games'))


@bp_game.route('/delete/<int:id>')
@validate_user_logged_in
def delete(id: int):
    if DB_ENGINE == 'memory':
        Game.delete(id=id, catalog=game_catalog)
        flash('Game was deleted successfuly!', 'success')
    elif DB_ENGINE == 'mysql':
        flash('DB Engine mysql not implemented yet!', 'warning')
    else:
        flash('No DB Engine was setted. Game still in memory', 'error')

    return redirect(url_for('bp_game.list_games'))
