from typing import Type

from django.contrib.auth import get_user_model

from . import FactoryProtocol, Factory
from ..repositories.model import UserCounter
from ..services import CounterProtocol, UserServiceProtocol, UserService, Service


class UserFactoryProtocol(FactoryProtocol):
    _counter_class: Type[UserCounter]

    @classmethod
    def get_counter(cls) -> CounterProtocol: ...

    @classmethod
    def get_service(cls) -> UserServiceProtocol: ...


class UserFactory(Factory):
    _model = get_user_model()
    _service_class: Type[Service] = UserService
    _service: UserServiceProtocol | None = None
    _counter_class: Type[UserCounter] = UserCounter

    @classmethod
    def get_service(cls) -> UserServiceProtocol:
        if cls._service is None:
            cls._service = cls._service_class(
                cls.get_crud_handler(),
                cls._counter_class(cls._model))
        return cls._service
