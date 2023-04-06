"""Protocols and implementations of Currency service."""
from typing import Protocol, Any

import requests
from django.conf import settings

from .crud import CRUDProtocol
from .services import ServiceProtocol, AbstractService


class StockServiceProtocol(ServiceProtocol, Protocol):

    @staticmethod
    def request_currencies() -> dict[str, Any]: ...

    def update_currencies(self) -> None: ...


class CurrencyService(AbstractService):
    def __init__(self, crud: CRUDProtocol):
        self._crud = crud

    @staticmethod
    def request_currencies() -> dict[str, Any]:
        currencies = requests.get(settings.CURRENCIES_API_URL).json()['rates']

        return currencies

    def update_currencies(self) -> None:
        currencies = self.request_currencies()
        main_currencies = {'USD': currencies.pop('RUB'), 'RUB': 1}
        for currency in currencies:
            self._crud.post(name=currency, value=1 / currencies[currency] * main_currencies['USD'])

        for currency in main_currencies:
            self._crud.post(name=currency, value=main_currencies[currency])
