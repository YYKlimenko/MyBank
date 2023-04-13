from typing import Any, Protocol

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet

from app.models import Asset, Account, Property, AssetCategory


class RepositoryProtocol(Protocol):
    model: models.Model | Any = ...

    def get(self, many: bool = False, prefetch_all=False, **filter_fields) -> QuerySet: ...

    def post(self, **fields) -> None: ...

    def delete(self, pk: int | str) -> None: ...

    def update(self, pk: int | str, data: dict[str, Any]): ...


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

    def update(self, pk: int | str, data: dict[str, Any]):
        self.get(pk=pk).update(**data)


class UserRepository(AbstractRepository):
    model = get_user_model()


class AssetRepository(AbstractRepository):
    model = Asset


class AssetCategoryRepository(AbstractRepository):
    model = AssetCategory


class AccountRepository(AbstractRepository):
    model = Account


class PropertyRepository(AbstractRepository):
    model = Property
