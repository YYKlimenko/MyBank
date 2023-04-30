"""Protocols and implementations of classes to request and update data."""
import abc
from typing import Protocol, Any

from ...repositories import BulkHandlerProtocol


class RequesterProtocol(Protocol):
    """The protocol to implement in Requester classes."""
    _URL: str

    def __call__(self) -> list[Any] | dict[str, Any]: ...


class UpdaterProtocol(Protocol):
    """The protocol to implement in Updater classes."""
    _requester: RequesterProtocol
    _handler: BulkHandlerProtocol

    def __call__(self, init: bool = False) -> None: ...


class Requester(abc.ABC):
    """The abstract class to use in implementations of RequesterProtocol."""
    _URL: str

    def __call__(self) -> list[Any] | dict[str, Any]: ...


class Updater(abc.ABC):
    """The abstract class to use in implementations of UpdaterProtocol."""

    def __init__(self, requester: RequesterProtocol, handler: BulkHandlerProtocol):
        self._requester = requester
        self._handler = handler

    def __call__(self, init: bool = False) -> None: ...
