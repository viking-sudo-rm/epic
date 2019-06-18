from overrides import overrides

from .base import NextSceneType, Scene
from ..events import UpdateEvent
from ..stanzas.base import Stanza


class StanzaScene(Scene):
    """Display text and then transition."""

    def __init__(self, stanza: Stanza, next_scene: NextSceneType):
        self._next_scene = next_scene
        self._stanza = stanza

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "TEXT", "=" * 10)
        text = self._stanza.generate(event)
        print(text)
        input()
        event.epic.add_stanza(text)
        return self.get_scene(self._next_scene, event)
