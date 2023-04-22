"""The Base Repository protocols and its implementations."""
from typing import Protocol

from .handlers import CRUDProtocol, BulkHandlerProtocol


class CRUDRepositoryProtocol(Protocol):
    """The repository protocol to make crud operations."""
    crud: CRUDProtocol


class BulkCRUDRepositoryProtocol(Protocol):
    """The repository protocol to make crud operations and operations with bulk."""
    crud: CRUDProtocol
    bulk_handler: BulkHandlerProtocol


class CRUDRepository:
    """The Base Repository class to maker crud operations."""

    def __init__(self, crud: CRUDProtocol):
        self.crud = crud


class BulkCRUDRepository:
    """The Base Repository class to make crud operations and operations with bulk."""

    def __init__(self, crud: CRUDProtocol, bulk_handler: BulkHandlerProtocol):
        self.crud = crud
        self.bulk_handler = bulk_handler
