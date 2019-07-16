from overrides import overrides
from typing import List

from .base import Scene
from ..entities import Entity
from ..events import UpdateEvent
from ..interface.commands import QuitCommand, SayCommand
from ..interface.dialog import DialogOption
from .location import LocationScene
from ..stanzas.base import Stanza


class DialogScene(Scene):

    _CMD_MAPPING = {
        "quit": QuitCommand(),
        "say": SayCommand(),
    }

    def __init__(self,
                 stanza: Stanza,
                 entity: Entity,
                 options: List[DialogOption] = []):
        self._stanza = stanza
        self._entity = entity
        self._options = options

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "DIALOG", "=" * 10)
        text = self._stanza.generate(event)
        event.epic.add_stanza(text)
        print(text)
        
        if self._options:
            for idx, option in enumerate(self._options):
                print("%d. %s\n" % (idx, option))
            next_scene = self._parse_and_exec_cmd(event)
            if next_scene is not None:
                return next_scene

        else:
            input()
        
        return LocationScene(self._entity.location)
