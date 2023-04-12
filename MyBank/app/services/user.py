"""Protocols and implementations of User service."""
from typing import Protocol, Any

from .crud import CRUDProtocol

from .services import Service, ServiceProtocol
from ..models import UserProtocol


class CounterProtocol(Protocol):
    """The protocol to implement in Counter classes."""

    @staticmethod
    def get_sum(user: UserProtocol) -> dict[str, Any]: ...


class UserServiceProtocol(ServiceProtocol, Protocol):
    _counter: CounterProtocol

    @staticmethod
    def get_sum(user_id: int) -> dict[str, Any]: ...


class Counter:
    @staticmethod
    def get_sum(user: UserProtocol) -> dict[str, Any]:
        data = {'accounts': 0, 'properties': 0}
        for account in user.accounts.all():
            data['accounts'] += account.count * account.currency.value
        for property_ in user.properties.all():
            data['properties'] += property_.value
        data['total'] = sum((data['accounts'], data['properties']))
        return data


class UserService(Service):
    def __init__(self, crud: CRUDProtocol, counter: CounterProtocol):
        super().__init__(crud)
        self._counter = counter

    def get_sum(self, user_id: int):
        user = self.crud.get(id=user_id)
        return {
            'username': user.username,
            'result': self._counter.get_sum(user),
        }
