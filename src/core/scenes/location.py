from overrides import overrides

from .base import Scene
from ..events import CommandEvent, UpdateEvent
from ..interface.commands import HelpCommand, QuitCommand, InteractCommand
from ..interface.commands import TalkCommand, SailCommand
from ..location import Location
from ..stanzas.base import Stanza


class LocationScene(Scene):

    _CMD_MAPPING = {
        "quit": QuitCommand(),
        "help": HelpCommand(),
        "interact": InteractCommand(),
        "talk": TalkCommand(),
        "sail": SailCommand(),
    }

    def __init__(self,
                 location: Location,
                 enter_stanza: Stanza = None,
                 always_announce: bool = False):
        self.location = location
        self._enter_stanza = enter_stanza
        self._always_announce = always_announce

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "LOCATION", "=" * 10)
        print("Location:", self.location.placename)
        print("Entities:", self.location._entities)

        self.location.update(event)
        if self._enter_stanza is not None and (self.location.first_visit or
                                               self._always_announce):
            # TODO: Switch this so that Locations can store an enter scene, and
            # LocationScenes can store an optional additional stanza.
            text = self._enter_stanza.generate(event,
                                               CITY=self.location.placename)
            print(text)
            event.epic.add_stanza(text)
        self.location.first_visit = False

        words = input("Action: ").lower().split(" ")
        print()
        cmd = words[0]
        args = words[1:]
        cmd_event = CommandEvent(event, cmd, args, self._CMD_MAPPING)
        if cmd in self._CMD_MAPPING:
            return self._CMD_MAPPING[cmd](cmd_event)
        else:
            print("Unknown command.")
            return self
