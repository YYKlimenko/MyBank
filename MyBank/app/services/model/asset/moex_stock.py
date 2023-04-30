"""Protocols and implementations of Moex stocks service."""
from typing import Any

import requests
from django.conf import settings

from app.repositories import BulkHandlerProtocol
from ...utils import RequesterProtocol


class MoexStockRequester:
    """The implementation of AbstractRequester to ge moex stocks."""
    _URL = settings.STOCK_API_URL

    def __call__(self) -> list[Any] | dict[str, Any]:
        currencies = requests.get(self._URL).json()['marketdata']['data']
        return currencies


class MoexStockUpdater:
    """The implementation of AbstractUpdater to update moex stocks."""

    def __init__(self, requester: RequesterProtocol, handler: BulkHandlerProtocol):
        self._requester = requester
        self._handler = handler

    def __call__(self, init: bool = False) -> None:
        bulk = [{'name': stock[0], 'description': stock[0], 'value': stock[1], 'category_id': 'moex_stock'}
                for stock in self._requester()]
        return self._handler.create(bulk) if init else self._handler.update(bulk)
