"""Protocols and implementations for common Service."""

from typing import Protocol, Any

from ..repositories import CRUDProtocol
from .utils import RequesterProtocol, UpdaterProtocol


class ServiceProtocol(Protocol):
    crud: CRUDProtocol


class AssetServiceProtocol(ServiceProtocol, Protocol):
    _requester: RequesterProtocol
    _updater: UpdaterProtocol

    def update(self, init: bool = False, data: dict[str, Any] | None = None): ...


class Service:

    def __init__(self, crud: CRUDProtocol):
        self.crud = crud


class AssetService(Service):

    def __init__(self, crud: CRUDProtocol, updater: UpdaterProtocol, requester: RequesterProtocol):
        super().__init__(crud)
        self._requester = requester
        self._updater = updater

    def update(self, init: bool = False, data: dict[str, Any] | None = None):
        return self._updater(data or self._requester(), init)
