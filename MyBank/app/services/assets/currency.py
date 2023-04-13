"""Protocols and implementations of Assets service."""
from typing import Any

import requests
from django.conf import settings

from ..crud import CRUDProtocol
from ..requester import RequesterProtocol


class CurrencyRequester:
    """The implementation of AbstractRequester for Currency."""
    _URL = settings.CURRENCIES_API_URL

    def __call__(self) -> list[Any] | dict[str, Any]:
        currencies = requests.get(self._URL).json()['rates']
        return currencies


class CurrencyUpdater:
    """The implementation of AbstractUpdater for Currencies."""
    def __call__(self, requester: RequesterProtocol, crud: CRUDProtocol) -> None:
        data = requester()
        main_currencies = {'USD': data.pop('RUB'), 'RUB': 1}
        for currency in data:
            crud.post(
                name=currency,
                value=1 / data[currency] * main_currencies['USD'],
                category_id='currency'
            )

        for currency in main_currencies:
            crud.post(name=currency, value=main_currencies[currency], category_id='currency')
