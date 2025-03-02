from asyncio import gather
from typing import TYPE_CHECKING, Optional
from uuid import uuid4

if TYPE_CHECKING:
    from .types import Event
    from .types import Listener as Listener_

    Listener = Listener_[Event]
from ..utils import wrapped_sync


class Controller:
    def __init__(self):
        self.registry: dict[type["Event"], list[tuple[str, "Listener"]]] = {}

    def subscribe(self, event_type: type["Event"], listener: "Listener") -> str:
        id = str(uuid4())
        data = (id, listener)
        if not event_type in self.registry:
            self.registry[event_type] = [data]
        else:
            self.registry[event_type].append(data)
        return id

    def clear(self, id: str, event_type: Optional[type["Event"]] = None):
        for listeners in (
            [self.registry[event_type]] if event_type else self.registry.values()
        ):
            for index, (listener_id, _) in enumerate(listeners):
                if id == listener_id:
                    listeners.pop(index)
                    return True
        return False

    async def trigger(self, event: "Event"):
        type_event = type(event)
        if not type_event in self.registry:
            return

        def fathers():
            for type, listeners in self.registry.items():
                if isinstance(event, type):
                    for _, listener in listeners:
                        yield listener

        generator = (wrapped_sync(listener, event) for listener in fathers())
        await gather(*generator)
