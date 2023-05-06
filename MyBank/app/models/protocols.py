from typing import Protocol


class AssetProtocol(Protocol):
    value: float


class AccountProtocol(Protocol):
    asset: AssetProtocol
    count: int


class PropertyProtocol(Protocol):
    value: float


class UserProtocol(Protocol):

    class Accounts(Protocol):
        @staticmethod
        def all() -> list[AccountProtocol]: ...

    class Properties(Protocol):
        @staticmethod
        def all() -> list[PropertyProtocol]: ...

    username: str
    accounts: Accounts = Accounts
    properties: Properties


class ModelProtocol(Protocol):
    class Manager(Protocol):
        @staticmethod
        def filter(*args, **kwargs): ...

        @staticmethod
        def get(*args, **kwargs): ...

        @staticmethod
        def bulk_create(*args, **kwargs): ...

        @staticmethod
        def bulk_update(*args, **kwargs): ...

    objects: Manager = Manager

    def __call__(self, *args, **kwargs): ...


class UserModelProtocol(ModelProtocol, Protocol):
    class Manager(ModelProtocol.Manager, Protocol):
        @staticmethod
        def create_user(*args, **kwargs) -> None: ...

    objects: Manager = Manager
