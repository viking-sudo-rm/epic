import random
from typing import Callable, List, Text

from .events import InteractEvent, UpdateEvent
from .interface.dialog import DialogOption
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
            interact_event = InteractEvent(event, self)
            return self._callback_fn(interact_event)
        else:
            print("There's nothing to do here.")
            return None

    def kill(self):
        if self.location is not None:
            self.location.remove_entity(self)

    def __repr__(self):
        return "Entity(%s)" % self.name


class Person(Entity):

    def __init__(self,
                 name,
                 pronoun=Pronoun.MASCULINE,
                 dialog_name: Text = None,
                 dialog_options: List[DialogOption] = [],
                 attributes: List[Text] = [],
                 **kwargs):
        super().__init__(name, **kwargs)
        self.pronoun = pronoun
        self.dialog_name = dialog_name
        # TODO: Can probably refactor how DialogScenes are created.
        self.dialog_options = dialog_options
        self.lover = None
        self.attributes = attributes

    def add_attribute(self, attribute: Text):
        self.attributes.append(attribute)

    @property
    def random_attribute(self):
        if len(self.attributes) == 0:
            return "Heroic"
        else:
            return random.choice(self.attributes)


class Object(Entity):
    pass
