from app import db

# from helper import GameAttribute, GameCategory, GameConsole


class GamesDB(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    console = db.Column(db.String(16), nullable=False)

    def __str__(self) -> str:
        return f'DB [{self.category}] **{self.name}** ({self.id}) can be played in {self.console}'

    def __repr__(self) -> str:
        return self.__str__()

    # TODO implement all CRUURD method and list by
