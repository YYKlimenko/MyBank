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
        main_currencies = {'USD': currencies.pop('RUB'), 'RUB': currencies.pop('USD')}
        currencies = {currency: 1 / currencies[currency] * main_currencies['USD'] for currency in currencies}
        currencies.update(main_currencies)
        return currencies


class CurrencyUpdater:
    """The implementation of AbstractUpdater for Currencies."""

    def __init__(self, handler: BulkHandlerProtocol):
        self._handler = handler

    def __call__(self, data: dict[str, Any], init: bool = False) -> None:
        bulk = {
            currency:
                {
                    'value': data[currency],
                    'category_id': 'currency'
                }
            for currency in data
        }
        return self._handler.create(bulk) if init else self._handler.update(bulk, ['value'])
