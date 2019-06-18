from abc import ABCMeta, abstractmethod
from typing import Any, Callable, Text, Union

from ..events import UpdateEvent


class Scene(metaclass=ABCMeta):

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


NextSceneType = Union[Text, Callable[[UpdateEvent], Text]]
