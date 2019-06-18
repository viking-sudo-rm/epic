from overrides import overrides

from .base import Scene
from ..events import UpdateEvent
from ..stanzas.base import Stanza


class TragedyScene(Scene):
    """When a player loses instead of reaching an ending."""

    def __init__(self, stanza: Stanza):
        self._stanza = stanza

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "TRAGEDY", "=" * 10)
        text = self._stanza.generate(event)
        print(text)
        event.epic.add_stanza(text)
        input()
        return None
