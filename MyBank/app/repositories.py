from typing import Any, Protocol

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet

from app.models import Currency, Account


class RepositoryProtocol(Protocol):
    model: models.Model = ...

    def get(self, many: bool = False, prefetch_all=False, **filter_fields) -> QuerySet:
        ...

    def post(self, fields: dict[str, Any]) -> None:
        ...


class AbstractRepository(RepositoryProtocol):

    def get(self, many: bool = False, prefetch_all=False, **filter_fields) -> QuerySet:
        instances = self.model.objects.filter(**filter_fields).select_related()
        if prefetch_all:
            instances = instances.prefetch_related()
        return instances if many else instances[0]

    def post(self, fields: dict[str, Any]) -> None:
        instance = self.model(**fields)
        instance.save()


class UserRepository(AbstractRepository):
    model = get_user_model()


class CurrencyRepository(AbstractRepository):
    model = Currency


class AccountRepository(AbstractRepository):
    model = Account
