"""Protocols and implementations of classes to request and update data."""
import abc
from typing import Protocol, Any

from .crud import CRUDProtocol


class RequesterProtocol(Protocol):
    """The protocol to implement in Requester classes."""
    _URL: str

    def __call__(self) -> list[Any] | dict[str, Any]: ...


class UpdaterProtocol(Protocol):
    """The protocol to implement in Updater classes."""
    def __call__(self, requester: RequesterProtocol, crud: CRUDProtocol) -> None: ...


class Requester(abc.ABC):
    """The abstract class to use in implementations of RequesterProtocol."""
    _URL: str

    def __call__(self) -> list[Any] | dict[str, Any]: ...


class Updater(abc.ABC):
    """The abstract class to use in implementations of UpdaterProtocol."""
    def __call__(self, requester: RequesterProtocol, crud: CRUDProtocol) -> None: ...
