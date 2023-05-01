"""Protocols and implementations of User service."""
from typing import Protocol

from ...repositories import CRUDProtocol

from ..base import Service, ServiceProtocol
from ...repositories.handlers import CounterProtocol
from ...serializers import UserSerializer
from ...serializers.protcols import SerializerProtocol


class UserServiceProtocol(ServiceProtocol, Protocol):
    counter: CounterProtocol


class UserService(Service):
    _get_serializer: SerializerProtocol = UserSerializer

    def __init__(self, crud: CRUDProtocol, counter: CounterProtocol):
        super().__init__(crud)
        self.counter = counter
