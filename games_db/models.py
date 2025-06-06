from typing import Any, Optional

from app import db

# from helper import GameAttribute, GameCategory, GameConsole


class GamesDB(db.Model):
    """
    Same as game but data is saved in DB (mysql)
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    console = db.Column(db.String(16), nullable=False)

    def __str__(self) -> str:
        return f'DB [{self.category}] **{self.name}** ({self.id}) can be played in {self.console}'

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def show(id: int) -> Any:
        """
        Receives:
            id: int = id to find a GamesDB
        Returns:
            game: Optional[GamesDB] = A GamesDB if found. Otherwise, None.
        """
        game: Optional[GamesDB] = GamesDB.query.filter_by(id=id).first()
        if not game:
            print('No game with id #{id} found in DB')

        return game

    @staticmethod
    def save(game: Any) -> bool:
        """
        Receives:
            game: GamesDB = A full game to be saved in db. Category and console should be saved by their enum's value.
        Returns:
            result: bool = success: [True | False]
        """
        result: bool = False
        already_exist: GamesDB = GamesDB.query.filter_by(name=game.name, console=game.console).first()

        if not already_exist:
            db.session.add(game)
            db.session.commit()
            result = True
        else:
            print(f'Found game with name {game.name} ({game.id}) already in db!!')

        return result

    @staticmethod
    def update(game: Any) -> bool:
        """
        Receives:
            game: GamesDB = A full game with valid id to be updated.
        Returns:
            result: bool = success [True | False]
        """
        result: bool = False
        already_exist: GamesDB = GamesDB.query.filter_by(id=game.id).first()
        # TODO validate name and console before update

        if already_exist:
            db.session.add(game)
            db.session.commit()
            result = True
        else:
            print(f'Game #{game.id} do not exist in db. Should update only existent game!')

        return result

    @staticmethod
    def delete(id: int) -> bool:
        """
        Receives:
            id: int = id of game to be delete. Should exist in DB!
        Returns:
            result: bool = success [True | False]
        """
        result: bool = False
        already_exist: GamesDB = GamesDB.query.filter_by(id=id).first()

        if already_exist:
            GamesDB.query.filter_by(id=id).delete()
            db.session.commit()
            result = True
        else:
            print(f'Game #{id} do not exist in db. Should update only existent game!')

        return result
