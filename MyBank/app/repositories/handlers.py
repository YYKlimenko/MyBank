"""The Base Class to handle operations with DB."""
from typing import Any, Protocol

from django.db import models
from django.db.models import QuerySet

from app.models import Asset
from app.models.protocols import ModelProtocol


class CRUDProtocol(Protocol):
    """CRUD protocol to make create, retrieve, update, delete operations."""
    model: ModelProtocol

    def get(self, serializer, many=False, prefetch_all=True, **filter_fields) -> Any: ...

    def post(self, **fields) -> None: ...

    def delete(self, pk: str | int) -> None: ...

    def update(self, pk: int | str, data: dict[str, Any]): ...


class BulkHandlerProtocol(Protocol):
    """The protocol to make operations with bilk."""
    model: ModelProtocol

    def create(self, bulk: list[Any]) -> None:
        ...

    def update(self, bulk: list[Any]) -> None:
        ...


class CRUDHandler:
    """The implementation of the CRUD protocol."""

    def __init__(self, model: ModelProtocol):
        self.model: ModelProtocol = model

    def get(self, serializer, many: bool = True, prefetch_all=False, **filter_fields) -> QuerySet:
        instances = self.model.objects.filter(**filter_fields).select_related()
        if prefetch_all:
            instances = instances.prefetch_related()
        return serializer(instances, many=True).data if many else serializer(instances[0]).data

    def post(self, **fields) -> None:
        instance = self.model(**fields)
        instance.save()

    def delete(self, pk: int | str) -> None:
        self.model.objects.get(pk=pk).delete()

    def update(self, pk: int | str, data: dict[str, Any]):
        self.model.objects.get(pk=pk).update(**data)


class BulkHandler:
    """The implementation of the BulkHandler protocol."""

    def __init__(self, model: ModelProtocol):
        self.model = model

    def create(self, bulk: list[Any]) -> None:
        self.model.objects.bulk_create([self.model(**kwargs) for kwargs in bulk])

    def update(self, bulk: list[Any]) -> None:
        self.model.objects.bulk_update([self.model(**kwargs) for kwargs in bulk])
