from typing import Callable

from events import UpdateEvent
from utils import overrides


class Entity:

    """A person or object in the world."""

    def __init__(self, name, position=None):
        self.name = name
        self.position = position

    def __repr__(self):
        return "Entity(%s)" % self.name

    def interact(self, event: UpdateEvent):
        pass


class Person(Entity):

    @overrides(Entity)
    def interact(self, event: UpdateEvent):
        quote = "Yo boi, you talking to %s?" % self.name
        print("%s: %s" % (self.name, quote))
        event.epic.add_stanza("And %s said:\n\t%s" % (self.name, quote))


class Object(Entity):

    def __init__(self,
                 name,
                 position=None,
                 callback_fn: Callable[[UpdateEvent], None] = None):
        super().__init__(name, position)
        self._callback_fn = callback_fn

    @overrides(Entity)
    def interact(self, event: UpdateEvent):
        if self._callback_fn is not None:
            return self._callback_fn(event)
