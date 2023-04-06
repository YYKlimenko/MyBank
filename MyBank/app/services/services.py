"""Protocols and implementations for common Service."""

import abc
from typing import Protocol, Any

from django.db.models import QuerySet

from .crud import CRUDProtocol
from .requester import RequesterProtocol, UpdaterProtocol


class ServiceProtocol(Protocol):
    def get(self, many=False, prefetch_all=True, **filter_fields) -> QuerySet: ...

    def post(self, **fields) -> None: ...


class TicketServiceProtocol(ServiceProtocol, Protocol):
    _requester: RequesterProtocol
    _updater: UpdaterProtocol

    def request_currencies(self) -> dict[str, Any]: ...

    def update_currencies(self) -> None: ...


class AbstractService(abc.ABC):
    _crud: CRUDProtocol

    def get(self, many=False, prefetch_all=True, **filter_fields) -> QuerySet:
        return self._crud.get(many, prefetch_all, **filter_fields)

    def post(self, **fields) -> None:
        return self._crud.post(**fields)


class Service(AbstractService):
    def __init__(self, crud: CRUDProtocol):
        self._crud = crud
