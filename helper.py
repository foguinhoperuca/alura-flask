from enum import StrEnum
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


class GameAttribute(StrEnum):
    pass


class GameCategory(GameAttribute):
    ADVENTURE = 'Adventure'
    FIGHT = 'Fight'
    GENERAL = 'General'
    HACK_N_SLASH = 'Hack and Slash'
    PUZZLE = 'Puzzle'
    RPG = 'rpg'
    STRATEGY = 'Strategy'
    ZOMBIE = 'Zombie'


class GameConsole(GameAttribute):
    ATARI = 'atari'
    PC = 'pc'
    PS1 = 'ps1'
    PS2 = 'ps2'
    PS3 = 'ps3'
    PS4 = 'ps4'
    PS5 = 'ps5'
    N64 = 'n64'
    SNES = 'snes'
    NES = 'nes'
