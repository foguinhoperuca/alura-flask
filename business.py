from enum import StrEnum
from typing import Any, Dict, List


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


class Game:
    def __init__(self, name: str, category: GameCategory = GameCategory.GENERAL, console: GameConsole = GameConsole.PC) -> None:
        self._name: str = name
        self._category: GameCategory = category
        self._console: GameConsole = console

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, vl: str) -> None:
        self._name = vl

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, vl: str) -> None:
        self._category = vl

    @property
    def console(self) -> str:
        return self._console

    @console.setter
    def console(self, vl: str) -> None:
        self._console = vl

    def __str__(self) -> str:
        return f'[{self.category}] **{self.name}** can be played in {self.console}'

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def order_by(games: List[Any], attr: GameAttribute = GameConsole) -> Dict[GameAttribute, List[Any]]:
        """
        Order an list of games by console or category (Game Attribute).
        Params:
            games: List[Game] = a list of games that should be ordered.
            attr: GameAttribute = An game attribute that could be [GameConsole | GameList]
        Returns:
            Dict of games (list) using the game attribute as key.

        """
        ordered_games: Dict[GameAttribute, list[Game]] = {}
        keys: List[GameAttribute]
        attribute: str

        if issubclass(attr, GameConsole):
            keys = [g.console for g in games]
            attribute = 'console'
        elif issubclass(attr, GameCategory):
            keys = [g.category for g in games]
            attribute = 'category'
        else:
            raise Exception(f'No GameAttribute found for: {type(attr)}')

        for value in list(set(keys)):
            ordered_games[value] = [game for game in games if getattr(game, attribute) == value]

        return ordered_games


def get_initial_catalog() -> List[Game]:
    """Seed data to start app and test"""
    return [
        Game(name='God of War V', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS5),
        Game(name='God of War IV', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS4),
        Game(name='God Of War III', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS3),
        Game(name='God of War II', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS2),
        Game(name='God of War I', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS1),
        Game(name='The Last of Us part I', category=GameCategory.ZOMBIE, console=GameConsole.PS3),
        Game(name='The Last of Us part II', category=GameCategory.ZOMBIE, console=GameConsole.PS4),
        Game(name='Zelda\'s Majora\'s Mask', category=GameCategory.ADVENTURE, console=GameConsole.N64),
        Game(name='Zelda Ocarina of Time', category=GameCategory.ADVENTURE, console=GameConsole.N64)
    ]


class User:
    def __init__(self, name: str, username: str, password: str) -> None:
        self._name: str = name
        self._username: str = username
        self._password: str = password

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, vl: str) -> None:
        self._name = vl

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, vl: str) -> None:
        self._username = vl

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, vl) -> None:
        self._password = vl

    def __str__(self) -> str:
        return f'[{self._username}] {self._name}'

    def __repr__(self) -> str:
        return f'[{self._username}] {self._name} :: {self._password}'

    def authenticate(self, username: str, password: str) -> bool:
        if self._username == username and self._password == password:
            return True

        return False


def get_users() -> Dict[str, User]:
    user_01: User = User(name='Jonh Doe', username='jonh_doe', password='A12345678a')
    user_02: User = User(name='Jane Doe', username='jane_doe', password='a87654321A')

    return {
        user_01.username: user_01,
        user_02.username: user_02
    }
