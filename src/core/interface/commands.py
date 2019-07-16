from abc import ABCMeta, abstractmethod
from overrides import overrides
from typing import Text

from ..entities import Person
from ..events import CommandEvent
from ..location import Sea
from ..scenes.base import Scene


class Command(metaclass=ABCMeta):

    @abstractmethod
    def __call__(self, event: CommandEvent) -> Scene:
        raise NotImplementedError

    @abstractmethod
    def help(self) -> Text:
        raise NotImplementedError

    @staticmethod
    def _print_too_many_args(cmd_name):
        print("Too many arguments for %s." % cmd_name)

    @staticmethod
    def _same_scene(cmd_event: CommandEvent) -> Scene:
        return cmd_event.update_event.scene


class QuitCommand(Command):

    @overrides
    def __call__(self, event: CommandEvent) -> Scene:
        if len(event.args) == 0:
            return None
        else:
            self._print_too_many_args(event.cmd)
            return event.update_event.scene

    @overrides
    def help(self) -> Text:
        return "End the current story."


class HelpCommand(Command):

    @overrides
    def __call__(self, event: CommandEvent) -> Scene:
        if len(event.args) == 0:
            cmds = event.cmd_mapping.keys()
            print(", ".join(cmds))
            print("Type 'help CMD' to get more information about CMD.")
        elif len(event.args) == 1:
            if event.args[0] in event.cmd_mapping.keys():
                help_text = event.cmd_mapping[event.args[0]].help()
                print(help_text)
        else:
            self._print_too_many_args(event.cmd)
        return self._same_scene(event)

    @overrides
    def help(self) -> Text:
        return "Show a list of commands, or more info about a certain command."


class InteractCommand(Command):

    @overrides
    def __call__(self, event: CommandEvent) -> Scene:
        if len(event.args) != 1:
            self._print_too_many_args(event.cmd)
            return self._same_scene(event)

        location = event.update_event.scene.location
        entity = location.get_entity(event.args[0])
        if entity is None:
            print("Invalid entity name: %s." % event.args[0])
        else:
            next_scene = entity.interact(event.update_event)
            if next_scene is not None:
                return next_scene

        return self._same_scene(event)

    @overrides
    def help(self) -> Text:
        return "Interact with an entity in your current location."


class TalkCommand(Command):

    @overrides
    def __call__(self, event: CommandEvent) -> Scene:
        if len(event.args) != 1:
            self._print_too_many_args(event.cmd)
            return self._same_scene(event)

        location = event.update_event.scene.location
        entity = location.get_entity(event.args[0])
        if entity is None:
            print("Invalid entity name: %s." % event.args[0])
        elif not isinstance(entity, Person):
            print("You can only talk to people.")
        elif entity.dialog_name is None:
            print("%s has nothing to say." % entity.name)
        else:
            stanza = event.update_event.stanzas[entity.dialog_name]
            dialog_scene_type = event.update_event.dialog_scene_type
            return dialog_scene_type(stanza, entity)

        return self._same_scene(event)

    @overrides
    def help(self) -> Text:
        return "Talk to an entity in your current location."


class SailCommand(Command):

    _DIRECTIONS = {
        "north": lambda location: location.north_neighbor,
        "east": lambda location: location.east_neighbor,
        "south": lambda location: location.south_neighbor,
        "west": lambda location: location.west_neighbor,
    }

    @overrides
    def __call__(self, event: CommandEvent) -> Scene:
        if len(event.args) != 1:
            self._print_too_many_args(event.cmd)
            return self._same_scene(event)

        location = event.update_event.scene.location
        if not isinstance(location, Sea):
            print("You cannot sail on land!")
            return self._same_scene(event)

        for direction, neighbor_fn in self._DIRECTIONS.items():
            if event.args[0] == direction:
                neighbor = neighbor_fn(location)
                if neighbor is None:
                    print("There is nothing to the %s." % direction)
                    return self._same_scene(event)
                location_scene_type = event.update_event.location_scene_type
                return location_scene_type(neighbor)

        print("Invalid direction for sailing: %s." % event.args[0])
        return self._same_scene(event)

    @overrides
    def help(self) -> Text:
        return "Sail north, east, south, or west (only while on the sea)."
