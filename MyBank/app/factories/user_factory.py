from typing import Protocol, Type

from . import FactoryProtocol, Factory
from ..services import CounterProtocol, UserServiceProtocol, Counter, UserService, Service


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

    @classmethod
    def get_counter(cls) -> CounterProtocol:
        if cls._counter is None:
            cls._counter = cls._counter_class()
        return cls._counter

    @classmethod
    def get_service(cls) -> UserServiceProtocol:
        if cls._service is None:
            cls._service = cls._service_class(cls.get_crud_handler(), cls.get_counter())
        return cls._service
