from typing import Callable, Text

from .events import UpdateEvent
from .pronouns import Pronoun


class Entity:

    """A person or object in the world."""

    def __init__(self,
                 name: Text,
                 location=None,
                 callback_fn: Callable[[UpdateEvent], None] = None):
        self.name = name
        self.location = location
        self._callback_fn = callback_fn

    def interact(self, event: UpdateEvent):
        if self._callback_fn is not None:
            return self._callback_fn(event)
        else:
            print("There's nothing to do here.")
            return None

    def kill(self):
        if self.location is not None:
            self.location.remove_entity(self)

    def __repr__(self):
        return "Entity(%s)" % self.name


class Person(Entity):

    def __init__(self, *args, pronoun=Pronoun.MASCULINE, **kwargs):
        super().__init__(*args, **kwargs)
        self.pronoun = pronoun


class Object(Entity):
    pass
        
