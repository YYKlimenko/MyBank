from typing import Protocol


class CurrencyProtocol(Protocol):
    value: float


class AccountProtocol(Protocol):
    currency: CurrencyProtocol
    count: int


class PropertyProtocol(Protocol):
    value: float


class UserProtocol(Protocol):

    class Accounts:
        @staticmethod
        def all() -> list[AccountProtocol]: ...

    class Properties:
        @staticmethod
        def all() -> list[PropertyProtocol]: ...

    username: str
    accounts = Accounts
    properties: Properties

