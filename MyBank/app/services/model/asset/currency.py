"""Protocols and implementations of Assets service."""
from typing import Any

import requests  # type: ignore
from django.conf import settings  # type: ignore

from ...utils import RequesterProtocol, Requester
from ....repositories import BulkHandlerProtocol


class CurrencyRequester(Requester):
    """The implementation of AbstractRequester for Currency."""

    def __call__(self) -> list[Any] | dict[str, Any]:
        currencies = requests.get(self._url).json()['rates']
        return currencies


class CurrencyUpdater:
    """The implementation of AbstractUpdater for Currencies."""

    def __init__(self, requester: RequesterProtocol, handler: BulkHandlerProtocol):
        self._requester = requester
        self._handler = handler

    def __call__(self, init: bool = False) -> None:
        data = self._requester()
        data.pop('USD')
        main_currencies = {'USD': data.pop('RUB'), 'RUB': 1}
        bulk = [
            {
             'name': currency,
             'value': 1 / data[currency] * main_currencies['USD'],
             'category_id': 'currency'
            }
            for currency in data
        ]

        bulk.extend(
            [{'name': currency, 'value': main_currencies[currency], 'category_id': 'currency'}
             for currency in main_currencies]
        )
        return self._handler.create(bulk) if init else self._handler.update(bulk)
