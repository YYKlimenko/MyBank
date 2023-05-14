"""Protocols and implementations of Moex stocks service."""
from typing import Any, Protocol

import requests  # type: ignore

from app.repositories import BulkHandlerProtocol
from ...utils import RequesterProtocol, Requester
from ...utils.updater import Updater, UpdaterProtocol


class MoexStockRequester(Requester):
    """The implementation of AbstractRequester to ge moex stocks."""

    def __call__(self) -> dict[str, Any]:
        currencies = requests.get(self._url).json()['marketdata']['data']
        currencies = {instance[0]: instance[1] for instance in currencies}
        return currencies


class MoexUpdaterProtocol(UpdaterProtocol, Protocol):
    _category_id: str


class MoexStockUpdater(Updater):
    """The implementation of AbstractUpdater to update moex stocks."""

    def __init__(self, requester: RequesterProtocol, handler: BulkHandlerProtocol, category_id: str):
        super().__init__(requester, handler)
        self._category_id = category_id

    def __call__(self, init: bool = False, data: dict[str, Any] | None = None) -> None:
        data = data or self._requester()
        data = {key: {'value': data[key], 'description': key, 'category_id': self._category_id} for key in data}
        return self._handler.create(data) if init else self._handler.update(
            data, ['description', 'value', 'category_id']
        )
