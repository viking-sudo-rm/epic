from overrides import overrides

from .base import Scene
from ..entities import Entity
from ..events import UpdateEvent
from .location import LocationScene
from ..stanzas.base import Stanza


class DialogScene(Scene):

    def __init__(self, stanza: Stanza, entity: Entity):
        self._stanza = stanza
        self._entity = entity

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "DIALOG", "=" * 10)
        text = self._stanza.generate(event)
        event.epic.add_stanza(text)
        print(text)
        input()
        return LocationScene(self._entity.location)
