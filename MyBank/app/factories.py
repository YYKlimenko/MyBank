from typing import Protocol
from logging import getLogger

from django.conf import settings

from app.repositories import (
    RepositoryProtocol, UserRepository, CurrencyRepository, AccountRepository, PropertyRepository
)
from app.services import (
    ServiceProtocol, CounterProtocol, Counter, UserService, UserServiceProtocol, Service, TicketServiceProtocol,
    CurrencyService
)
from app.services.currency import CurrencyRequester, CurrencyUpdater
from app.services.requester import RequesterProtocol, UpdaterProtocol


class FactoryProtocol(Protocol):
    repository: RepositoryProtocol
    service: ServiceProtocol

    @staticmethod
    def get_repository() -> RepositoryProtocol: ...

    @classmethod
    def get_service(cls) -> ServiceProtocol: ...


class TicketFactoryProtocol(FactoryProtocol, Protocol):
    requester: RequesterProtocol
    updater: UpdaterProtocol

    @staticmethod
    def get_requester() -> RequesterProtocol: ...

    @staticmethod
    def get_updater() -> UpdaterProtocol: ...

    @classmethod
    def get_service(cls) -> TicketServiceProtocol: ...


class CurrencyFactory:

    @staticmethod
    def get_requester() -> RequesterProtocol:
        return CurrencyRequester(settings.CURRENCIES_API_URL)

    @staticmethod
    def get_updater() -> UpdaterProtocol:
        return CurrencyUpdater()

    @staticmethod
    def get_repository() -> RepositoryProtocol:
        return CurrencyRepository()

    @classmethod
    def get_service(cls) -> TicketServiceProtocol:
        return CurrencyService(cls.get_repository(), cls.get_requester(), cls.get_updater())


class AccountFactory:

    @staticmethod
    def get_repository() -> RepositoryProtocol:
        return AccountRepository()

    @classmethod
    def get_service(cls) -> ServiceProtocol:
        return Service(cls.get_repository())


class PropertyFactory:

    @staticmethod
    def get_repository() -> RepositoryProtocol:
        return PropertyRepository()

    @classmethod
    def get_service(cls) -> ServiceProtocol:
        return Service(cls.get_repository())


class UserFactory:

    @staticmethod
    def get_repository() -> RepositoryProtocol:
        return UserRepository()

    @staticmethod
    def get_service() -> UserServiceProtocol:
        repository: RepositoryProtocol = UserFactory.get_repository()
        counter: CounterProtocol = Counter()
        return UserService(repository, counter)
