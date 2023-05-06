"""Protocols and implementations of classes to request data."""
import abc
from typing import Protocol, Any


class RequesterProtocol(Protocol):
    """The protocol to implement in Requester classes."""
    _url: str

    def __call__(self) -> list[Any] | dict[str, Any]: ...


class Requester(abc.ABC):
    """The abstract class to use in implementations of RequesterProtocol."""

    def __init__(self, url: str) -> None:
        self._url = url

    @abc.abstractmethod
    def __call__(self) -> list[Any] | dict[str, Any]: ...
