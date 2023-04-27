from typing import Protocol, Any


class SerializerProtocol(Protocol):
    data: dict[str, Any]

    def __call__(self, *args, **kwargs): ...
