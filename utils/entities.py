from typing import Callable, Text

from .events import UpdateEvent


class Entity:

    """A person or object in the world."""

    def __init__(self,
                 name: Text,
                 location=None,
                 callback_fn: Callable[[UpdateEvent], None] = None,
                 male=True):
        self.name = name
        self._male = male
        self.location = location
        self._callback_fn = callback_fn

    @property
    def nom_pronoun(self):
        return "he" if self._male else "she"

    @property
    def acc_pronoun(self):
        return "him" if self._male else "her"

    def __repr__(self):
        return "Entity(%s)" % self.name

    def interact(self, event: UpdateEvent):
        if self._callback_fn is not None:
            return self._callback_fn(event)
        else:
            print("There's nothing to do here.")
            return None

    def kill(self):
        if self.location is not None:
            self.location.remove_entity(self)


class Person(Entity):
    pass


class Object(Entity):
    pass
        
