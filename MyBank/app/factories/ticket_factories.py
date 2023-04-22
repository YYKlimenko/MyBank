"""The protocol, the abstract class and implementations to create family of objects."""
from typing import Protocol, Type

from . import FactoryProtocol
from . import Factory
from ..models import Asset
from ..models.protocols import ModelProtocol
from ..repositories import BulkHandler
from ..services import (
    AssetServiceProtocol, RequesterProtocol, UpdaterProtocol, AssetService,
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


class AssetFactory(Factory):
    _model: Asset | ModelProtocol
    _service_class: Type[AssetService] = AssetService
    _service: AssetServiceProtocol | None = None
    _bulk_handler_class: Type[BulkHandler] = BulkHandler
    _requester_class: Type[Requester]
    _updater_class: Type[Updater]
    _updater: UpdaterProtocol | None = None

    @classmethod
    def get_updater(cls) -> UpdaterProtocol:
        if cls._updater is None:
            cls._updater = cls._updater_class(
                cls._requester_class(),
                cls._bulk_handler_class(cls._model)
            )
        return cls._updater

    @classmethod
    def get_service(cls) -> AssetServiceProtocol:
        if cls._service is None:
            cls._service = cls._service_class(cls.get_crud_handler(), cls.get_updater())
        return cls._service


class CurrencyFactory(AssetFactory):
    _requester_class: Type[RequesterProtocol] = CurrencyRequester
    _updater_class: Type[UpdaterProtocol] = CurrencyUpdater


class StockFactory(AssetFactory):
    _requester_class: Type[MoexStockRequester] = MoexStockRequester
    _updater_class: Type[MoexStockUpdater] = MoexStockUpdater
