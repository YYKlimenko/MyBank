"""Protocols and implementations of Currency service."""
from typing import Protocol, Any

import requests
from django.conf import settings

from .crud import CRUDProtocol
from .requester import RequesterProtocol, UpdaterProtocol
from .services import AbstractService


class CurrencyRequester:
    def __init__(self, url: str):
        self._url = url

    def __call__(self) -> dict[str, Any]:
        currencies = requests.get(self._url).json()['rates']
        return currencies


class CurrencyUpdater:
    def __call__(self, data: dict[str, Any], crud: CRUDProtocol) -> None:
        main_currencies = {'USD': data.pop('RUB'), 'RUB': 1}
        for currency in data:
            crud.post(name=currency, value=1 / data[currency] * main_currencies['USD'])

        for currency in main_currencies:
            crud.post(name=currency, value=main_currencies[currency])


class CurrencyService(AbstractService):
    def __init__(self, crud: CRUDProtocol, requester: RequesterProtocol, updater: UpdaterProtocol):
        self._crud = crud
        self._requester = requester
        self._updater = updater

    def request_currencies(self) -> dict[str, Any]:
        return self._requester()

    def update_currencies(self) -> None:
        return self._updater(self.request_currencies(), self._crud)
