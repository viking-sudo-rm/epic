from abc import ABCMeta, abstractmethod
from typing import Any, Union, Callable, Dict, List, Text

from entities import Entity
from epic import Epic
from events import UpdateEvent
from utils import overrides
from location import Location
from stanzas import Stanza


class Scene(metaclass=ABCMeta):

    @abstractmethod
    def update(self, event: UpdateEvent):
        """Game logic update (physics, position, etc.)."""
        raise NotImplementedError


NextSceneType = Union[Text, Callable[[UpdateEvent], Text]]


class StanzaScene(Scene):
    """Display text and then transition."""

    def __init__(self, stanza: Stanza, next_scene: NextSceneType):
        self._next_scene = next_scene
        self._stanza = stanza

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "TEXT", "=" * 10)
        text = self._stanza.generate(event)
        print(text)
        input()
        event.epic.add_stanza(text)
        return event.get_scene(self._next_scene)


class SelectionScene(Scene):
    """Choose a character at the beginning."""

    def __init__(self,
                 prompt: Text,
                 options: List[Any],
                 value_fn: Callable[[Any], Text],
                 select_fn: Callable[[Epic], Callable[[Any], None]],
                 stanzas: Dict[Text, Stanza],
                 next_scene: NextSceneType):
        self._next_scene = next_scene
        self._prompt = prompt
        self._options = options
        self._value_fn = value_fn
        self._select_fn = select_fn
        self._stanzas = stanzas

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "SELECTION", "=" * 10)
        print(self._prompt, self._options)
        query = input("Select: ").lower()
        for option in self._options:
            if query == self._value_fn(option):
                selection = option
                break
        self._select_fn(event.epic)(selection)
        stanza_name = "select_" + self._value_fn(selection)
        if stanza_name in self._stanzas:
            text = self._stanzas[stanza_name].generate(event)
            print(text)
            input()
            event.epic.add_stanza(text)
        return event.get_scene(self._next_scene)


class LocationScene(Scene):

    def __init__(self, location: Location, enter_stanza: Stanza = None):
        self._location = location
        self._enter_stanza = enter_stanza
        self._first_visit = True

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "LOCATION", "=" * 10)
        print("Location:", self._location.placename)
        print("Entities:", self._location._entities)

        self._location.update(event)
        if self._first_visit and self._enter_stanza is not None:
            text = self._enter_stanza.generate(event, CITY=self._location.placename)
            print(text)
            event.epic.add_stanza(text)
        self._first_visit = False

        words = input("Action: ").lower().split(" ")
        print()
        action = words[0]
        if action == "quit":
            return None
        elif action == "interact":
            for entity in self._location._entities:
                if entity.name.lower() == words[1]:
                    next_scene = entity.interact(event)
                    return self if next_scene is None else next_scene
        elif action == "fight":
            for entity in self._location._entities:
                if entity.name.lower() == words[1]:
                    self._location._entities.remove(entity)
        else:
            print("Unknown command.")
        return self


class DuelScene(Scene):

    def __init__(self, enemy: Entity, next_scene: NextSceneType):
        self._enemy = enemy
        self._next_scene = next_scene

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "DUEL", "=" * 10)
        print(event.epic.hero, "versus", self._enemy)
        input()
        self._enemy.kill()
        print("You win!")
        return event.get_scene(self._next_scene)

    @property
    def location(self):
        return self._enemy.location


class EndScene(Scene):

    def __init__(self, stanza: Stanza, character: Entity):
        self._stanza = Stanza
        self._character = character

    @overrides(Scene)
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "ENDING", "=" * 10)
        text = self._stanza.generate(event)
        print(text)
        print("Unlocked", character)
        input()
        event.epic.add_stanza(text)
        return None
