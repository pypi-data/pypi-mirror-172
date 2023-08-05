from typing import Any

from insanic.utils import Container

from .fields import Field


class SerializationError(Exception):
    pass

class Serializer(Container):
    FIELD_BASE_CLASS = Field

    def __new__(cls, *args, many=False, **kwargs): # type: ignore
        if many:
            # @TODO: Ignoring type due https://github.com/python/mypy/issues/6799
            return ListSerializer(serializer_cls=cls, *args, **kwargs)  # type: ignore[misc]
        return super().__new__(cls)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        # Adding support for nested serializers
        for attribute in dir(self):
            if isinstance(getattr(self, attribute), self.__class__.__bases__ + (ListSerializer, )):
                self._field_names.append(attribute)

    async def serialize(self, data: dict) -> dict:
        return {
            field_name: await field.serialize(field_value)
            for field_name, field_value, field in self._field_values(data)
        }

class ListSerializer:
    serializer_class: type[Serializer]

    def __init__(self, serializer_cls: type[Serializer]) -> None:
        self.serializer_class = serializer_cls

    async def serialize(self, data: dict) -> list[dict]:
        serializer = self.serializer_class()

        return [
            await serializer.serialize(entity)
            for entity in data
        ]
