"""Protocols and implementations of classes to request and update data."""
from typing import Protocol, Any

from .crud import CRUDProtocol


class RequesterProtocol(Protocol):
    _url: str

    def __call__(self) -> dict[str, Any]: ...


class UpdaterProtocol(Protocol):
    def __call__(self, data: dict[str, Any], crud: CRUDProtocol) -> None: ...
