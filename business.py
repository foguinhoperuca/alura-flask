from typing import Dict


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
