from typing import Protocol, Type

from . import FactoryProtocol, Factory
from ..repositories import UserRepository
from ..services import CounterProtocol, UserServiceProtocol, Counter, CRUD, UserService, Service


class UserFactoryProtocol(FactoryProtocol):
    _counter_class: Type[Counter]
    _counter: CounterProtocol | None

    @classmethod
    def get_counter(cls) -> CounterProtocol: ...

    @classmethod
    def get_service(cls) -> UserServiceProtocol: ...


class UserFactory(Factory):
    _service_class: Type[Service] = UserService
    _service: UserServiceProtocol | None = None
    _counter_class: Type[Counter] = Counter
    _counter: CounterProtocol | None = None
    _repository_class: Type[UserRepository] = UserRepository

    @classmethod
    def get_counter(cls) -> CounterProtocol:
        if cls._counter is None:
            cls._counter = cls._counter_class()
        return cls._counter

    @classmethod
    def get_service(cls) -> UserServiceProtocol:
        if cls._service is None:
            crud = CRUD(cls.get_repository())
            cls._service = cls._service_class(crud, cls.get_counter())
        return cls._service
