"""The protocol, the abstract class and implementations to create family of objects."""
from typing import Protocol, Type

from django.conf import settings

from . import FactoryProtocol
from .factories import AbstractFactory
from ..services import TicketServiceProtocol, RequesterProtocol, UpdaterProtocol, ServiceProtocol, CRUD


class TicketFactoryProtocol(FactoryProtocol, Protocol):
    _service_class: Type[TicketServiceProtocol]
    _service: TicketServiceProtocol
    _repository_class = Protocol[RequesterProtocol]
    _requester: RequesterProtocol
    _updater_class = Protocol[UpdaterProtocol]
    _updater: UpdaterProtocol

    @classmethod
    def get_requester(cls) -> RequesterProtocol: ...

    @classmethod
    def get_updater(cls) -> UpdaterProtocol: ...

    @classmethod
    def get_service(cls) -> TicketServiceProtocol: ...


class TicketFactory(AbstractFactory):
    _service_class: Protocol[TicketServiceProtocol]
    _service: TicketServiceProtocol | None = None
    _requester_class = Protocol[RequesterProtocol]
    _requester: RequesterProtocol | None = None
    _updater_class = Protocol[UpdaterProtocol]
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
