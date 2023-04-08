"""Protocols and implementations for common Service."""

import abc
from typing import Protocol, Any

from django.db.models import QuerySet

from .crud import CRUDProtocol
from .requester import RequesterProtocol, UpdaterProtocol
from ..repositories import RepositoryProtocol


class ServiceProtocol(Protocol):
    crud: CRUDProtocol

    def __init__(self, crud: CRUDProtocol, **kwargs): ...


class TicketServiceProtocol(CRUDProtocol, Protocol):
    _requester: RequesterProtocol
    _updater: UpdaterProtocol

    def request_currencies(self) -> dict[str, Any]: ...

    def update_currencies(self) -> None: ...


class Service:

    def __init__(self, crud: CRUDProtocol):
        self.crud = crud
