"""Protocols and implementations of User service."""
from typing import Protocol

from ...repositories import CRUDProtocol

from ..base import Service, ServiceProtocol
from ...repositories.handlers import CounterProtocol


class UserServiceProtocol(ServiceProtocol, Protocol):
    counter: CounterProtocol


class UserService(Service):

    def __init__(self, crud: CRUDProtocol, counter: CounterProtocol):
        super().__init__(crud)
        self.counter = counter
