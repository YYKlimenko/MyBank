"""Protocols and implementations of Moex stocks service."""
from typing import Any

import requests
from django.conf import settings

from ..requester import RequesterProtocol
from ..crud import CRUDProtocol


class MoexStockRequester:
    """The implementation of AbstractRequester to ge moex stocks."""
    _URL = settings.STOCK_API_URL

    def __call__(self) -> list[Any] | dict[str, Any]:
        currencies = requests.get(self._URL).json()['marketdata']['data']
        return currencies


class MoexStockUpdater:
    """The implementation of AbstractUpdater to update moex stocks."""
    def __call__(self, requester: RequesterProtocol, crud: CRUDProtocol) -> None:
        for stock in requester():
            crud.post(name=stock[0], description=stock[0], value=stock[1], category_id='moex_stock')
