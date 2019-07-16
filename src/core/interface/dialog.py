from typing import Text

from ..events import UpdateEvent
from ..scenes.base import Scene

class DialogOption:

    def __init__(self, text: Text, callback_fn):
        self.text = text
        self._callback_fn = callback_fn

    def __call__(self, event: UpdateEvent) -> Scene:
        hero_attribute = event.epic.hero.random_attribute
        event.epic.add_stanza("Our %s hero spoke:" % hero_attribute)
        event.epic.add_stanza(option.text)
        # The callback should return None if we want to go back to the entity's
        # location.
        return callback_fn(event)
