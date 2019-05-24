from typing import Callable, Text

from .events import UpdateEvent


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

    def __init__(self, *args, male=True, **kwargs):
        super().__init__(*args, **kwargs)
        self._male = male
    
    @property
    def nom_pronoun(self):
        return "he" if self._male else "she"

    @property
    def acc_pronoun(self):
        return "him" if self._male else "her"

    @property
    def title_nom_pronoun(self):
        return self.nom_pronoun.title()

    @property
    def title_acc_pronoun(self):
        return self.acc_pronoun.title()


class Object(Entity):
    pass
        
