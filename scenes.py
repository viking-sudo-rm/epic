from abc import ABCMeta, abstractmethod
from typing import Any, Callable, List, Text

from epic import Epic
from utils import overrides
from location import Location, Entity


class UpdateEvent:

    def __init__(self, epic, last_scene):
        self.epic = epic
        self.last_scene = last_scene


class Scene(metaclass=ABCMeta):

    def update(self, event: UpdateEvent):
        """Game logic update (physics, position, etc.)."""
        pass


class TextScene(Scene):
    """Display text and then transition."""

    def __init__(self, next_scene: Scene, text: Text):
        self._next_scene = next_scene
        self._text = text

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "TEXT", "=" * 10)
        print(self._text)
        input()
        event.epic.add_stanza(self._text)
        return self._next_scene


class SelectionScene(Scene):
    """Choose a character at the beginning."""

    def __init__(self,
                 next_scene: Scene,
                 prompt: Text,
                 options: List[Any],
                 select_fn: Callable[[Epic], Callable[[Any], None]]):
        self._next_scene = next_scene
        self._prompt = prompt
        self._options = options
        self._select_fn = select_fn

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "SELECTION", "=" * 10)
        print(self._prompt, self._options)
        index = int(input("Select index: "))
        selection = self._options[index]
        self._select_fn(event.epic)(selection)
        event.epic.add_stanza("Hail, %s!" % selection.name)
        return self._next_scene


class LocationScene(Scene):

    def __init__(self, location: Location):
        self._location = location

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "LOCATION", "=" * 10)
        print("Location:", self._location.placename)
        print("Entities:", self._location._entities)

        self._location.update(event)
        if event.last_scene is not self:
            event.epic.add_stanza("Alas, we enter bright " + self._location.placename)

        words = input("Action: ").lower().split(" ")
        print()
        action = words[0]
        if action == "quit":
            return None
        elif action == "kill":
            for entity in self._location._entities:
                if entity.name.lower() == words[1]:
                    self._location._entities.remove(entity)
        return self


class EndScene(Scene):

    def __init__(self, text: Text, character: Entity):
        self._text = text
        self._character = character

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "ENDING", "=" * 10)
        print(self._text)
        print("Unlocked", character)
        input()
        event.epic.add_stanza(self._text)
        return None
