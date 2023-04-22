"""The protocol, the abstract class and implementations to create family of objects."""
from typing import Protocol, Type

from app.models import Account, Property, AssetCategory
from app.models.protocols import ModelProtocol
from app.repositories import CRUDRepositoryProtocol, CRUDHandler, CRUDProtocol
from app.services import ServiceProtocol, Service


class FactoryProtocol(Protocol):
    """The protocol to implementation in factory classes."""
    _repository_class: Type[CRUDRepositoryProtocol]
    _service_class: Type[Service]
    _repository: CRUDRepositoryProtocol | None
    _service: ServiceProtocol | None

    @classmethod
    def get_repository(cls) -> CRUDRepositoryProtocol: ...

    @classmethod
    def get_service(cls) -> ServiceProtocol: ...


class Factory:
    """The Abstract Factory class to use in implementations."""
    _model: ModelProtocol | None = ...
    _crud_handler: CRUDProtocol | None = None
    _service_class: Type[Service] = Service
    _service: ServiceProtocol | None = None

    @classmethod
    def get_crud_handler(cls) -> CRUDProtocol:
        if cls._crud_handler is None:
            cls._crud_handler = CRUDHandler(cls._model)
        return cls._crud_handler

    @classmethod
    def get_service(cls) -> ServiceProtocol:
        if cls._service is None:
            cls._service = cls._service_class(cls.get_crud_handler())
        return cls._service


class AccountFactory(Factory):
    """The implementation of AbstractFactory and FactoryProtocol for Account model."""
    _model: ModelProtocol = Account


class PropertyFactory(Factory):
    """The implementation of AbstractFactory and FactoryProtocol for Property model."""
    _model: ModelProtocol = Property


class AssetCategoryFactory(Factory):
    """The implementation of AbstractFactory and FactoryProtocol for AssetCategory model."""
    _model: ModelProtocol = AssetCategory
