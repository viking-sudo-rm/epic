from abc import ABCMeta, abstractmethod
from overrides import overrides
from typing import Any, Union, Callable, List, Text
import random

from .entities import Entity, Person
from .epic import Epic
from .events import UpdateEvent
from .location import Location, Sea
from .stanzas.base import Stanza


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


class SelectionScene(Scene):
    """Choose a character at the beginning."""

    def __init__(self,
                 prompt: Text,
                 options: List[Any],
                 value_fn: Callable[[Any], Text],
                 select_fn: Callable[[Epic], Callable[[Any], None]],
                 next_scene: NextSceneType):
        self._next_scene = next_scene
        self._prompt = prompt
        self._options = options
        self._value_fn = value_fn
        self._select_fn = select_fn

    @overrides
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
        if stanza_name in event.stanzas:
            text = event.stanzas[stanza_name].generate(event)
            print(text)
            input()
            event.epic.add_stanza(text)
        return self.get_scene(self._next_scene, event)


class LocationScene(Scene):

    def __init__(self,
                 location: Location,
                 enter_stanza: Stanza = None,
                 always_announce: bool = False):
        self._location = location
        self._enter_stanza = enter_stanza
        self._always_announce = always_announce

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "LOCATION", "=" * 10)
        print("Location:", self._location.placename)
        print("Entities:", self._location._entities)

        self._location.update(event)
        if self._enter_stanza is not None and (self._location.first_visit or
                                               self._always_announce):
            # TODO: Switch this so that Locations can store an enter scene, and
            # LocationScenes can store an optional additional stanza.
            text = self._enter_stanza.generate(event,
                                               CITY=self._location.placename)
            print(text)
            event.epic.add_stanza(text)
        self._location.first_visit = False

        words = input("Action: ").lower().split(" ")
        print()
        action = words[0]
        args = words[1:]

        if action == "quit":
            return None

        elif action == "interact":
            for entity in self._location._entities:
                if entity.name.lower() == args[0]:
                    next_scene = entity.interact(event)
                    return self if next_scene is None else next_scene

        elif action == "talk":
            for entity in self._location._entities:
                if entity.name.lower() == args[0]:
                    if not isinstance(entity, Person):
                        print("You can only talk to people.")
                        return self
                    elif entity.dialog_name is None:
                        print("This character has nothing to say.")
                    else:
                        stanza = event.stanzas[entity.dialog_name]
                        return DialogScene(stanza, entity)

        elif action == "sail" and isinstance(self._location, Sea):
            if not isinstance(self._location, Sea):
                print("You cannot sail on land!")
                return self
            if args[0] == "north":
                if self._location.north_neighbor is None:
                    print("There is nothing to the north.")
                    return self
                return LocationScene(self._location.north_neighbor)
            elif args[0] == "east":
                if self._location.east_neighbor is None:
                    print("There is nothing to the east.")
                    return self
                return LocationScene(self._location.east_neighbor)
            elif args[0] == "south":
                if self._location.south_neighbor is None:
                    print("There is nothing to the south.")
                    return self
                return LocationScene(self._location.south_neighbor)
            elif args[0] == "west":
                if self._location.west_neighbor is None:
                    print("There is nothing to the west.")
                    return self
                return LocationScene(self._location.west_neighbor)
            else:
                print("Invalid direction for sailing: %s." % args[0])
                return self

        else:
            print("Unknown command.")
        return self


class DuelScene(Scene):

    def __init__(self, enemy: Entity, next_scene: NextSceneType):
        self._enemy = enemy
        self._next_scene = next_scene

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "DUEL", "=" * 10)
        print(event.epic.hero, "versus", self._enemy)
        input()
        self._enemy.kill()
        text = self.get_stock_duel_text(event)
        event.epic.add_stanza(text)
        print(text)
        return self.get_scene(self._next_scene, event)

    def get_stock_duel_text(self, event, weapon="lance"):
        """Return stock duel text picked uniformly at random from duel stanzas."""
        num_duels = sum(1 for name in event.stanzas if name.startswith("duels/stock"))
        duel_idx = random.randint(0, num_duels - 1)
        stanza = event.stanzas["duels/stock%d" % duel_idx]
        return stanza.generate(event,
                               ENEMY=self._enemy,
                               WEAPON=weapon)

    @property
    def location(self):
        return self._enemy.location


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


class EndScene(Scene):

    def __init__(self, stanza: Stanza, character: Entity):
        self._stanza = stanza
        self._character = character

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "ENDING", "=" * 10)
        text = self._stanza.generate(event)
        print(text)
        print("Unlocked", character)
        input()
        event.epic.add_stanza(text)
        return None
