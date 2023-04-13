"""The protocol, the abstract class and implementations to create family of objects."""
from typing import Protocol, Type

from app.repositories import (
    RepositoryProtocol, AccountRepository, PropertyRepository, AssetCategoryRepository
)
from app.services import CRUD, ServiceProtocol, Service


class FactoryProtocol(Protocol):
    """The protocol to implementation in factory classes."""
    _repository_class: Type[RepositoryProtocol]
    _service_class: Type[Service]
    _repository: RepositoryProtocol | None
    _service: ServiceProtocol | None

    @classmethod
    def get_repository(cls) -> RepositoryProtocol: ...

    @classmethod
    def get_service(cls) -> ServiceProtocol: ...


class Factory:
    """The Abstract Factory class to use in implementations."""
    _repository_class: Type[RepositoryProtocol]
    _service_class: Type[Service] = Service
    _repository: RepositoryProtocol | None = None
    _service: ServiceProtocol | None = None

    @classmethod
    def get_repository(cls) -> RepositoryProtocol:
        if cls._repository is None:
            cls._repository = cls._repository_class()
        return cls._repository

    @classmethod
    def get_service(cls) -> ServiceProtocol:
        if cls._service is None:
            crud = CRUD(cls.get_repository())
            cls._service = cls._service_class(crud)
        return cls._service


class AccountFactory(Factory):
    """The implementation of AbstractFactory and FactoryProtocol for Account model."""
    _repository_class: Type[RepositoryProtocol] = AccountRepository


class PropertyFactory(Factory):
    """The implementation of AbstractFactory and FactoryProtocol for Property model."""
    _repository_class: Type[RepositoryProtocol] = PropertyRepository


class AssetCategoryFactory(Factory):
    """The implementation of AbstractFactory and FactoryProtocol for AssetCategory model."""
    _repository_class: Type[RepositoryProtocol] = AssetCategoryRepository
