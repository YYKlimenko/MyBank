from typing import Protocol, Any

import requests

from django.conf import settings
from django.db import models
from django.db.models import QuerySet

from MyBank.metaclasses import Bean
from app.repositories import RepositoryProtocol


class CRUDProtocol(Protocol):
    def get(self, many=False, prefetch_all=True, **filter_fields) -> QuerySet: ...

    def post(self, **fields) -> None: ...


class CRUD(metaclass=Bean):
    def __init__(self, repository: RepositoryProtocol):
        self._repository = repository

    def get(self, many=False, prefetch_all=True, **filter_fields) -> QuerySet:
        return self._repository.get(many=many, prefetch_all=prefetch_all, **filter_fields)

    def post(self, **fields) -> None:
        return self._repository.post(**fields)


class CounterProtocol(Protocol):

    @staticmethod
    def get_sum(
            user: models.Model,
            count_accounts: bool = True,
            count_properties: bool = True
    ) -> dict[str, Any]: ...


class Counter(metaclass=Bean):

    @staticmethod
    def get_sum(
            user: models.Model,
            count_accounts: bool = True,
            count_properties: bool = True
    ):
        accounts = user.accounts.all()
        properties = user.properties.all()
        result = dict()

        for i in ('accounts', 'properties'):
            if n := locals().get(f'count_{i}'):
                result[i] = 0
                for j in locals().get(i):
                    result[i] += n.currency.value * getattr('count', n, 1)
        result['total'] = sum(result.values())

        return result


class CurrencyService(metaclass=Bean):
    def __init__(self, crud: CRUDProtocol):
        self.crud = crud

    @staticmethod
    def request_currencies():
        currencies = requests.get(settings.CURRENCIES_API_URL).json()['rates']
        currencies['USD'], currencies['RUB'] = currencies['RUB'], 1
        return currencies

    def update_currencies(self):
        currencies = self.request_currencies()
        for currency in currencies:
            self.crud.post(name=currency, value=1 / currencies[currency] * currencies['USD'])


class UserService:
    def __init__(self, crud: CRUDProtocol, counter: CounterProtocol):
        self.crud = crud
        self._counter = counter

    def get_sum(self, user_id: int):
        user = self.crud.get(id=user_id)
        return {
            'username': user.username,
            'result': self._counter.get_sum(user),
        }

