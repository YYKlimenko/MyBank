"""Protocols and implementations for common Service."""

from typing import Protocol

from ..repositories import CRUDProtocol
from .utils import UpdaterProtocol


class ServiceProtocol(Protocol):
    crud: CRUDProtocol


class AssetServiceProtocol(ServiceProtocol, Protocol):
    updater: UpdaterProtocol


class Service:

    def __init__(self, crud: CRUDProtocol):
        self.crud = crud


class AssetService(Service):

    def __init__(self, crud: CRUDProtocol, updater: UpdaterProtocol):
        super().__init__(crud)
        self.updater = updater
