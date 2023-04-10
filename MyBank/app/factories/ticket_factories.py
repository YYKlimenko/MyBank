"""The protocol, the abstract class and implementations to create family of objects."""
from typing import Protocol, Type

from . import FactoryProtocol
from . import Factory
from ..repositories import CurrencyRepository, StockRepository
from ..services import (
    TicketServiceProtocol, RequesterProtocol, UpdaterProtocol, CRUD, TicketService,
    CurrencyRequester, CurrencyUpdater
)
from ..services.requester import Requester, Updater
from ..services.stock import MoexStockRequester, MoexStockUpdater


class TicketFactoryProtocol(FactoryProtocol, Protocol):
    _service_class: Type[TicketService]
    _service: TicketServiceProtocol
    _requester_class = Type[Requester]
    _requester: RequesterProtocol
    _updater_class = Type[Updater]
    _updater: UpdaterProtocol

    @classmethod
    def get_requester(cls) -> RequesterProtocol: ...

    @classmethod
    def get_updater(cls) -> UpdaterProtocol: ...

    @classmethod
    def get_service(cls) -> TicketServiceProtocol: ...


class TicketFactory(Factory):
    _service_class: Type[TicketService] = TicketService
    _service: TicketServiceProtocol | None = None
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
    def get_service(cls) -> TicketServiceProtocol:
        if cls._service is None:
            crud = CRUD(cls.get_repository())
            cls._service = cls._service_class(crud, cls.get_requester(), cls.get_updater())
        return cls._service


class CurrencyFactory(TicketFactory):
    _service: TicketServiceProtocol | None = None
    _requester_class: Type[RequesterProtocol] = CurrencyRequester
    _updater_class: Type[UpdaterProtocol] = CurrencyUpdater
    _repository_class: Type[CurrencyRepository] = CurrencyRepository


class StockFactory(TicketFactory):
    _service: TicketServiceProtocol | None = None
    _requester_class: Type[MoexStockRequester] = MoexStockRequester
    _updater_class: Type[MoexStockUpdater] = MoexStockUpdater
    _repository_class: Type[StockRepository] = StockRepository
