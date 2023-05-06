"""Protocols and implementations of classes to request and update data."""
from abc import ABC, abstractmethod
from typing import Protocol

from app.repositories import BulkHandlerProtocol
from app.services.utils import RequesterProtocol


class UpdaterProtocol(Protocol):
    """The protocol to implement in Updater classes."""
    _requester: RequesterProtocol
    _handler: BulkHandlerProtocol

    def __call__(self, init: bool = False) -> None: ...


class Updater(ABC):
    """The abstract class to use in implementations of UpdaterProtocol."""

    def __init__(self, requester: RequesterProtocol, handler: BulkHandlerProtocol):
        self._requester = requester
        self._handler = handler

    @abstractmethod
    def __call__(self, init: bool = False) -> None: ...
