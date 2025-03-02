from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .base import Controller
    from .types import Event, Listener


def decorator_listener[
    E: Event
](controller: "Controller", event_type: type["Event"]) -> Callable[
    ["Listener[E]"], "Listener[E]"
]:
    def wrapper(listener: "Listener[E]") -> "Listener[E]":
        controller.subscribe(event_type=event_type, listener=listener)  # type: ignore
        return listener

    return wrapper
