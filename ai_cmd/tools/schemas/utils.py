from enum import Enum
from typing import Any


def typing_is_enum(annotation: Any) -> bool:
    """Checks if a type annotation is an enum."""
    try:
        return issubclass(annotation, Enum)
    except:
        return False


def get_enum_values(enum_type: type[Enum]) -> list[Any]:
    """Gets the values from an enum type."""
    return [e.value for e in enum_type]
