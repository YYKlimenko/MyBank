"""Protocols and implementations of classes to request and update data."""
from abc import ABC, abstractmethod
from typing import Protocol, Any

from app.repositories import BulkHandlerProtocol


class UpdaterProtocol(Protocol):
    """The protocol to implement in Updater classes."""
    _handler: BulkHandlerProtocol

    def __call__(self, data: dict[str, Any], init: bool = False) -> None: ...


class Updater(ABC):
    """The abstract class to use in implementations of UpdaterProtocol."""

    def __init__(self, handler: BulkHandlerProtocol):
        self._handler = handler

    @abstractmethod
    def __call__(self, data: dict[str, Any], init: bool = False) -> None: ...
