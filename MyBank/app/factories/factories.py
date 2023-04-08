"""The protocol, the abstract class and implementations to create family of objects."""
import abc
from typing import Protocol, Type

from app.repositories import RepositoryProtocol, AccountRepository, PropertyRepository
from app.services import CRUDProtocol, Service, CRUD, ServiceProtocol


class FactoryProtocol(Protocol):
    """The protocol to implementation in factory classes."""
    _repository_class: Type[RepositoryProtocol]
    _service_class: Type[ServiceProtocol]
    _repository: RepositoryProtocol | None
    _service: ServiceProtocol | None

    @staticmethod
    def get_repository() -> RepositoryProtocol: ...

    @classmethod
    def get_service(cls) -> CRUDProtocol: ...


class AbstractFactory(abc.ABC):
    """The Abstract Factory class to use in implementations."""
    _repository_class: Type[RepositoryProtocol]
    _service_class: Type[ServiceProtocol]
    _repository: RepositoryProtocol | None
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


class BaseServiceFactory(AbstractFactory):
    _service_class: Type[ServiceProtocol] = Service


class AccountFactory(BaseServiceFactory):
    """The implementation of AbstractFactory and FactoryProtocol for Account model."""
    _repository_class: Type[RepositoryProtocol] = AccountRepository


class PropertyFactory(BaseServiceFactory):
    """The implementation of AbstractFactory and FactoryProtocol for Property model."""
    _repository_class: Type[RepositoryProtocol] = PropertyRepository
