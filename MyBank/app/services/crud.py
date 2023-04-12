"""CRUD protocol to use in Service classes."""
from typing import Protocol, Any

from app.repositories import RepositoryProtocol


class CRUDProtocol(Protocol):
    """CRUD protocol to make create, retrieve, update, delete operations."""
    _repository: RepositoryProtocol

    def get(self, many=False, prefetch_all=True, **filter_fields) -> Any: ...

    def post(self, **fields) -> None: ...

    def delete(self, pk: str | int) -> None: ...


class CRUD:
    """Implementation of the CRUD protocol."""
    def __init__(self, repository: RepositoryProtocol):
        self._repository = repository

    def get(self, many=False, prefetch_all=True, **filter_fields) -> Any:
        return self._repository.get(many=many, prefetch_all=prefetch_all, **filter_fields)

    def post(self, **fields) -> None:
        return self._repository.post(**fields)

    def delete(self, pk: int | str) -> None:
        return self._repository.delete(pk=pk)
