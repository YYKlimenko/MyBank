"""Protocols and implementations of Moex stocks service."""
from typing import Any, Protocol

import requests  # type: ignore

from app.repositories import BulkHandlerProtocol
from ...utils import RequesterProtocol, Requester
from ...utils.updater import Updater, UpdaterProtocol


class MoexStockRequester(Requester):
    """The implementation of AbstractRequester to ge moex stocks."""

    def __call__(self) -> list[Any] | dict[str, Any]:
        currencies = requests.get(self._url).json()['marketdata']['data']
        return currencies


class MoexUpdaterProtocol(UpdaterProtocol, Protocol):
    _category_id: str


class MoexStockUpdater(Updater):
    """The implementation of AbstractUpdater to update moex stocks."""

    def __init__(self, requester: RequesterProtocol, handler: BulkHandlerProtocol, category_id: str):
        super().__init__(requester, handler)
        self._category_id = category_id

    def __call__(self, init: bool = False) -> None:
        bulk = [
            {'name': stock[0], 'description': stock[0], 'value': stock[1], 'category_id': self._category_id}
            for stock in self._requester()
        ]
        return self._handler.create(bulk) if init else self._handler.update(bulk)
