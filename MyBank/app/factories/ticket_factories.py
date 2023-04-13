"""The protocol, the abstract class and implementations to create family of objects."""
from typing import Protocol, Type

from . import FactoryProtocol
from . import Factory
from ..repositories import AssetRepository
from ..services import (
    AssetServiceProtocol, RequesterProtocol, UpdaterProtocol, CRUD, AssetService,
    CurrencyRequester, CurrencyUpdater
)
from ..services.requester import Requester, Updater
from ..services.assets import MoexStockRequester, MoexStockUpdater


class AssetFactoryProtocol(FactoryProtocol, Protocol):
    _service_class: Type[AssetService]
    _service: AssetServiceProtocol
    _requester_class = Type[Requester]
    _requester: RequesterProtocol
    _updater_class = Type[Updater]
    _updater: UpdaterProtocol

    @classmethod
    def get_requester(cls) -> RequesterProtocol: ...

    @classmethod
    def get_updater(cls) -> UpdaterProtocol: ...

    @classmethod
    def get_service(cls) -> AssetServiceProtocol: ...


class TicketFactory(Factory):
    _service_class: Type[AssetService] = AssetService
    _service: AssetServiceProtocol | None = None
    _repository_class: Type[AssetRepository] = AssetRepository
    _repository: AssetRepository | None = None
    _requester_class: Type[Requester]
    _requester: RequesterProtocol | None = None
    _updater_class: Type[Updater]
    _updater: UpdaterProtocol | None = None

    @classmethod
    def get_requester(cls) -> RequesterProtocol:
        if cls._requester is None:
            cls._requester = cls._requester_class()
        return cls._requester

    @classmethod
    def get_updater(cls) -> UpdaterProtocol:
        if cls._updater is None:
            cls._updater = cls._updater_class()
        return cls._updater

    @classmethod
    def get_service(cls) -> AssetServiceProtocol:
        if cls._service is None:
            crud = CRUD(cls.get_repository())
            cls._service = cls._service_class(crud, cls.get_requester(), cls.get_updater())
        return cls._service


class CurrencyFactory(TicketFactory):
    _requester_class: Type[RequesterProtocol] = CurrencyRequester
    _updater_class: Type[UpdaterProtocol] = CurrencyUpdater


class StockFactory(TicketFactory):
    _requester_class: Type[MoexStockRequester] = MoexStockRequester
    _updater_class: Type[MoexStockUpdater] = MoexStockUpdater
