"""CRUD protocol and implementation."""
from typing import Protocol

from django.db.models import QuerySet

from MyBank.metaclasses import Bean
from app.repositories import RepositoryProtocol


class CRUDProtocol(Protocol):
    """CRUD protocol to make create, retrieve, update, delete operations."""
    def get(self, many=False, prefetch_all=True, **filter_fields) -> QuerySet: ...

    def post(self, **fields) -> None: ...


class CRUD(metaclass=Bean):
    """Implementation of CRUD protocol."""
    def __init__(self, repository: RepositoryProtocol):
        self._repository = repository

    def get(self, many=False, prefetch_all=True, **filter_fields) -> QuerySet:
        return self._repository.get(many=many, prefetch_all=prefetch_all, **filter_fields)

    def post(self, **fields) -> None:
        return self._repository.post(**fields)
