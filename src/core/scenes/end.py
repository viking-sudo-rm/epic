from overrides import overrides

from .base import Scene
from ..entities import Entity
from ..events import UpdateEvent
from ..stanzas.base import Stanza


class EndScene(Scene):

    def __init__(self, stanza: Stanza, character: Entity):
        self._stanza = stanza
        self._character = character

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "ENDING", "=" * 10)
        text = self._stanza.generate(event)
        print(text)
        print("Unlocked", self._character)
        input()
        event.epic.add_stanza(text)
        return None
