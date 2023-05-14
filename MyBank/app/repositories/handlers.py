"""The Base Class to handle operations with DB."""
from typing import Any, Protocol

from django.core.exceptions import FieldError as DjangoFieldError, FieldDoesNotExist

from app.models.protocols import ModelProtocol
from app.repositories.exceptions import FieldError
from app.serializers.protocols import SerializerProtocol


class CRUDProtocol(Protocol):
    """CRUD protocol to make create, retrieve, update, delete operations."""
    model: ModelProtocol

    def get(
            self, serializer: SerializerProtocol, many=False, prefetch_all=True, **filter_fields
    ) -> dict[str, Any] | list[dict[str, Any]]: ...

    def post(self, **fields) -> None: ...

    def delete(self, pk: str | int) -> None: ...

    def update(self, pk: int | str, data: dict[str, Any]): ...


class BulkHandlerProtocol(Protocol):
    """The protocol to make operations with bilk."""
    model: ModelProtocol

    def create(self, bulk: dict[str, Any]) -> None:
        ...

    def update(self, bulk: dict[str, Any], fields: list[str]) -> None:
        ...


class CRUDHandler:
    """The implementation of the CRUD protocol."""

    def __init__(self, model: ModelProtocol):
        self.model: ModelProtocol = model

    def get(
            self, serializer: SerializerProtocol, many: bool = True, prefetch_all=False, **filter_fields
    ) -> dict[str, Any] | list[dict[str, Any]]:
        try:
            instances = self.model.objects.filter(**filter_fields).select_related()
            if prefetch_all:
                instances = instances.prefetch_related()
            return serializer(instances, many=True).data if many else serializer(instances[0]).data
        except DjangoFieldError as exception:
            raise FieldError(message=DjangoFieldError) from exception

    def post(self, **fields) -> None:
        instance = self.model(**fields)
        instance.save()

    def delete(self, pk: int | str) -> None:
        self.model.objects.get(pk=pk).delete()

    def update(self, pk: int | str, data: dict[str, Any]):
        try:
            self.model.objects.filter(pk=pk).update(**data)
        except (FieldDoesNotExist, ValueError, TypeError) as exception:
            raise FieldError(message=exception) from exception


class BulkHandler:
    """The implementation of the BulkHandler protocol."""

    def __init__(self, model: ModelProtocol):
        self.model = model

    def create(self, bulk: dict[str, Any]) -> None:
        try:
            self.model.objects.bulk_create([self.model(pk=key, **bulk[key]) for key in bulk])
        except (ValueError, TypeError) as exception:
            raise FieldError(message=exception) from exception

    def update(self, bulk: dict[str, Any], fields: list[str]) -> None:
        try:
            self.model.objects.bulk_update(
                [self.model(pk=key, **bulk[key]) for key in bulk],
                fields,
            )
        except (DjangoFieldError, ValueError, TypeError) as exception:
            raise FieldError(message=exception) from exception


class CounterProtocol(Protocol):
    model: ModelProtocol

    def get_sum(self, user_id: int) -> dict[str, Any]: ...
