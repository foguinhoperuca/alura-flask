from enum import StrEnum
from typing import Any, Dict, List, Optional, Set


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
    LATEST_ID: int = 0

    def __init__(self, name: str, category: GameCategory = GameCategory.GENERAL, console: GameConsole = GameConsole.PC) -> None:
        Game.LATEST_ID += 1
        self._id: int = Game.LATEST_ID
        self._name: str = name
        self._category: GameCategory = category
        self._console: GameConsole = console

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, vl: int) -> None:
        self._id = vl

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
        return f'[{self.category}] **{self.name}** ({self.id}) can be played in {self.console}'

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self):
        return hash(self._id)

    def __eq__(self, other) -> bool:
        return self.id == other.id

    @staticmethod
    def order_by(games: Set[Any], attr: GameAttribute = GameConsole) -> Dict[GameAttribute, List[Any]]:
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

    @staticmethod
    def find_game_in_catalog(id: int, catalog: List[Any]) -> Optional[Any]:
        """
        Search for a game (by id) in catalog and return it!
        Params:
            id: int = real id from game
            catalog: List[Game] = A list of games saved in memory
        Returns:
            Game = Game found in catalog. None otherwise.
        """
        found: List[Game] = [game for game in catalog if game.id == id]
        if len(found) == 0:
            print('[WARN] No game found in catalog!!')
            return None

        return found[0]

    @staticmethod
    def delete(id: int, catalog: List[Any]) -> None:
        original_len_catalog: int = len(catalog)
        found: Game = Game.find_game_in_catalog(id, catalog)
        if found is None:
            raise Exception('No game found in catalog!!')

        catalog.remove(found)

        actual_len_catalog: int = len(catalog)
        print(f'=== Removed with success === original: {original_len_catalog} vs. actual: {actual_len_catalog}')


def get_initial_catalog() -> Set[Game]:
    """Seed data to start app and test"""
    return {
        Game(name='God of War V', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS5),
        Game(name='God of War IV', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS4),
        Game(name='God Of War III', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS3),
        Game(name='God of War II', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS2),
        Game(name='God of War I', category=GameCategory.HACK_N_SLASH, console=GameConsole.PS1),
        Game(name='The Last of Us part I', category=GameCategory.ZOMBIE, console=GameConsole.PS3),
        Game(name='The Last of Us part II', category=GameCategory.ZOMBIE, console=GameConsole.PS4),
        Game(name='Zelda\'s Majora\'s Mask', category=GameCategory.ADVENTURE, console=GameConsole.N64),
        Game(name='Zelda Ocarina of Time', category=GameCategory.ADVENTURE, console=GameConsole.N64)
    }


def get_user(id: int, catalog: List[Game]) -> Game:
    return list(filter(lambda game: game.id == id, catalog))[0]


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
