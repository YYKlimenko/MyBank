from typing import Any, Protocol

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet

from app.models import Currency, Account, Property, Stock


class RepositoryProtocol(Protocol):
    model: models.Model | Any = ...

    def get(self, many: bool = False, prefetch_all=False, **filter_fields) -> QuerySet: ...

    def post(self, **fields) -> None: ...

    def delete(self, pk: int | str) -> None: ...


class AbstractRepository:
    model: models.Model | Any

    def get(self, many: bool = True, prefetch_all=False, **filter_fields) -> QuerySet:
        instances = self.model.objects.filter(**filter_fields).select_related()
        if prefetch_all:
            instances = instances.prefetch_related()
        return instances if many else instances[0]

    def post(self, **fields) -> None:
        instance = self.model(**fields)
        instance.save()

    def delete(self, pk: int | str) -> None:
        self.get(pk=pk).delete()


class UserRepository(AbstractRepository):
    model = get_user_model()


class CurrencyRepository(AbstractRepository):
    model = Currency


class AccountRepository(AbstractRepository):
    model = Account


class PropertyRepository(AbstractRepository):
    model = Property


class StockRepository(AbstractRepository):
    model = Stock
