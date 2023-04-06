from typing import Protocol
from logging import getLogger

from app.repositories import RepositoryProtocol, UserRepository, CurrencyRepository, AccountRepository, \
    PropertyRepository
from app.services.services import ServiceProtocol, CounterProtocol, Counter, UserService, UserServiceProtocol, \
    Service, CurrencyServiceProtocol, CurrencyService

logger = getLogger(__name__)


class FactoryProtocol(Protocol):

    @staticmethod
    def get_repository(self) -> RepositoryProtocol: ...

    @staticmethod
    def get_service(self) -> ServiceProtocol: ...


class CurrencyFactory:

    @staticmethod
    def get_repository() -> RepositoryProtocol:
        return CurrencyRepository()

    @staticmethod
    def get_service() -> CurrencyServiceProtocol:
        repository: RepositoryProtocol = CurrencyFactory.get_repository()
        return CurrencyService(repository)


class AccountFactory:

    @staticmethod
    def get_repository() -> RepositoryProtocol:
        return AccountRepository()

    @staticmethod
    def get_service() -> ServiceProtocol:
        repository: RepositoryProtocol = AccountFactory.get_repository()
        return Service(repository)


class PropertyFactory:

    @staticmethod
    def get_repository() -> RepositoryProtocol:
        return PropertyRepository()

    @staticmethod
    def get_service() -> ServiceProtocol:
        repository: RepositoryProtocol = PropertyFactory.get_repository()
        return Service(repository)


class UserFactory:

    @staticmethod
    def get_repository() -> RepositoryProtocol:
        return UserRepository()

    @staticmethod
    def get_service() -> UserServiceProtocol:
        repository: RepositoryProtocol = UserFactory.get_repository()
        counter: CounterProtocol = Counter()
        return UserService(repository, counter)
