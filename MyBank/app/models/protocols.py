from typing import Protocol


class AssetProtocol(Protocol):
    value: float


class AccountProtocol(Protocol):
    currency: AssetProtocol
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

