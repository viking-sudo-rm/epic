from overrides import overrides
from typing import List

from .base import Scene
from ..entities import Entity
from ..events import UpdateEvent
from ..interface.commands import HelpCommand, QuitCommand, SayCommand
from ..interface.dialog import DialogOption
from .location import LocationScene
from ..stanzas.base import Stanza


class DialogScene(Scene):

    _CMD_MAPPING = {
        "quit": QuitCommand(),
        "help": HelpCommand(),
        "say": SayCommand(),
    }

    def __init__(self, stanza: Stanza, entity: Entity):
        self._stanza = stanza
        self._entity = entity

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "DIALOG", "=" * 10)
        text = self._stanza.generate(event)
        event.epic.add_stanza(text)
        print(text)
        
        if self._entity.dialog_options:
            print()
            for idx, option in enumerate(self._entity.dialog_options):
                print("%d. %s\n" % (idx, option.text))
            return self._parse_and_exec_cmd(event)

        else:
            input()
        
        return LocationScene(self.location)

    def get_option(self, idx):
        return self._entity.dialog_options[idx]

    @property
    def location(self):
        return self._entity.location
