"""Protocols and implementations of User service."""
from typing import Protocol, Any

from .crud import CRUDProtocol
from .services import AbstractService, ServiceProtocol
from .. import models


class CounterProtocol(Protocol):

    @staticmethod
    def get_sum(
            user: models.Model,
            count_accounts: bool = True,
            count_properties: bool = True
    ) -> dict[str, Any]: ...


class UserServiceProtocol(ServiceProtocol, Protocol):
    _counter: CounterProtocol

    def get_sum(self, user_id: int) -> dict[str, Any]: ...


class UserService(AbstractService):
    def __init__(self, crud: CRUDProtocol, counter: CounterProtocol):
        self._crud = crud
        self._counter = counter

    def get_sum(self, user_id: int) -> dict[str, Any]:
        user = self.get(id=user_id)
        return {
            'username': user.username,
            'result': self._counter.get_sum(user),
        }
