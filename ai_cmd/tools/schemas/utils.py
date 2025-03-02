from enum import Enum
from typing import Any


def typing_is_list(annotation: Any) -> bool:
    """Checks if a type annotation is a list."""
    try:
        return hasattr(annotation, "__origin__") and annotation.__origin__ is list
    except:
        return False


def get_list_item_type(annotation: Any) -> Any:
    """Gets the item type of a list annotation."""
    try:
        return annotation.__args__[0]
    except:
        return str


def typing_is_enum(annotation: Any) -> bool:
    """Checks if a type annotation is an enum."""
    try:
        return issubclass(annotation, Enum)
    except:
        return False


def get_enum_values(enum_type: type[Enum]) -> list[Any]:
    """Gets the values from an enum type."""
    return [e.value for e in enum_type]
