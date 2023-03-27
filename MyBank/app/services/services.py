import requests

from django.conf import settings

from MyBank.metaclasses import Bean
from app.repositories import RepositoryProtocol


class ServiceProtocol:
    def __init__(self, repository: RepositoryProtocol): ...


class Service(metaclass=Bean):
    def __init__(self, repository: RepositoryProtocol):
        self.repository = repository


class CurrencyService(Service):

    @staticmethod
    def request_currencies():
        currencies = requests.get(settings.CURRENCIES_API_URL).json()['rates']
        currencies['USD'], currencies['RUB'] = currencies['RUB'], 1
        return currencies

    def update_currencies(self):
        currencies = self.request_currencies()
        for currency in currencies:
            self.repository.post(name=currency, value=currencies[currency])
