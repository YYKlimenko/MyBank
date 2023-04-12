"""Protocols and implementations for common Service."""

from typing import Protocol, Any

from .crud import CRUDProtocol
from .requester import RequesterProtocol, UpdaterProtocol


class ServiceProtocol(Protocol):
    crud: CRUDProtocol


class TicketServiceProtocol(ServiceProtocol, Protocol):
    _requester: RequesterProtocol
    _updater: UpdaterProtocol

    def request(self) -> list[Any] | dict[str, Any]: ...

    def update(self) -> None: ...


class Service:

    def __init__(self, crud: CRUDProtocol):
        self.crud = crud


class TicketService(Service):

    def __init__(self, crud: CRUDProtocol, requester: RequesterProtocol, updater: UpdaterProtocol):
        super().__init__(crud)
        self._requester = requester
        self._updater = updater

    def request(self) -> list[Any] | dict[str, Any]:
        return self._requester()

    def update(self) -> None:
        return self._updater(self._requester, self.crud)
