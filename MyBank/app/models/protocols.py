from typing import Protocol


class AssetProtocol(Protocol):
    value: float


class AccountProtocol(Protocol):
    asset: AssetProtocol
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


class ModelProtocol:
    class Manager:
        @staticmethod
        def filter(*args, **kwargs): ...

        @staticmethod
        def bulk_create(*args, **kwargs): ...

        @staticmethod
        def bulk_update(*args, **kwargs): ...

    objects = Manager

    def __call__(self, *args, **kwargs): ...