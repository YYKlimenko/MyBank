"""Protocols and implementations of classes to request data."""
from abc import ABC, abstractmethod
from typing import Protocol, Any


class RequesterProtocol(Protocol):
    """The protocol to implement in Requester classes."""
    _url: str

    def __call__(self) -> list[Any] | dict[str, Any]: ...


class Requester(ABC):
    """The abstract class to use in implementations of RequesterProtocol."""

    def __init__(self, url: str) -> None:
        self._url = url

    @abstractmethod
    def __call__(self) -> list[Any] | dict[str, Any]: ...
