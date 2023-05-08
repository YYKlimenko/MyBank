"""The Base Class to handle operations with DB."""
from typing import Any, Protocol

from app.models.protocols import ModelProtocol
from app.serializers.protocols import SerializerProtocol


class CRUDProtocol(Protocol):
    """CRUD protocol to make create, retrieve, update, delete operations."""
    model: ModelProtocol

    def get(self, serializer: SerializerProtocol, many=False, prefetch_all=True, **filter_fields) -> Any: ...

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

    def get(
            self, serializer: SerializerProtocol, many: bool = True, prefetch_all=False, **filter_fields
    ) -> dict[str, Any]:
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
        self.model.objects.filter(pk=pk).update(**data)


class BulkHandler:
    """The implementation of the BulkHandler protocol."""

    def __init__(self, model: ModelProtocol):
        self.model = model

    def create(self, bulk: list[Any]) -> None:
        self.model.objects.bulk_create([self.model(**kwargs) for kwargs in bulk])

    def update(self, bulk: dict[str, Any], fields: list[str]) -> None:
        self.model.objects.bulk_update(
            [self.model(pk=key, **bulk[key]) for key in bulk],
            fields,
        )


class CounterProtocol(Protocol):
    model: ModelProtocol

    def get_sum(self, user_id: int) -> dict[str, Any]: ...
