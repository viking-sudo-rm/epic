from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Text, Union

from ..events import CommandEvent, UpdateEvent


class Scene(metaclass=ABCMeta):

    # This should be overriden in superclasses with commands.
    _CMD_MAPPING = {}

    @abstractmethod
    def update(self, event: UpdateEvent):
        """Game logic update (physics, position, etc.)."""
        raise NotImplementedError

    def get_scene(self, name: Any, event: UpdateEvent):
        """Get next scene from a scene instance, name, or selector object."""
        if isinstance(name, Scene):
            return name
        elif callable(name):
            name = name(self)

        return event.scenes.get(name, None)

    def _parse_and_exec_cmd(self, event: UpdateEvent):
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


NextSceneType = Union[Text, Callable[[UpdateEvent], Text]]
