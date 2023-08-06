from typing import Any, Generic, Type, TypeVar, Union

T = TypeVar("T")


class StateMeta(type):
    kind: Type[T]

    def __getitem__(cls, item: Any) -> "StateMeta":
        cls.kind = item
        return cls


def _type_error(value: T, kind: Type) -> ValueError:
    return ValueError(
        f'Expected "{kind.__name__}", but updating with value ' f'"{str(value)}" of type "{type(value).__name__}"'
    )


class State(Generic[T], metaclass=StateMeta):
    kind: Type
    value: T

    def __init__(self, initial: T):
        if not isinstance(initial, self.kind):
            raise _type_error(initial, self.kind)
        self.value = initial

    def update(self, value):
        if not isinstance(value, self.kind):
            raise _type_error(value, self.kind)
        self.value = value
