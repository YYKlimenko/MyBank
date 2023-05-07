from typing import Protocol, Any


class SerializerNonInitProtocol(Protocol):

    def __call__(self, *args, **kwargs): ...


class SerializerInitProtocol(SerializerNonInitProtocol, Protocol):
    data: dict[str, Any]
    validated_data: dict[str, Any]

    def is_valid(self, *args, **kwargs): ...


SerializerProtocol = SerializerInitProtocol | SerializerNonInitProtocol
