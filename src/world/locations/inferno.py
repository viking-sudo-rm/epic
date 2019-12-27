from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import InteractEvent, UpdateEvent
from src.core.interface.dialog import DialogOption
from src.core.location import Location, Sea
from src.core.scenes.base import Scene
from src.core.scenes.dialog import DialogScene
from src.core.scenes.location import LocationScene
from src.core.scenes.stanza import StanzaScene


def _pehter_nation_callback_fn(update_event: UpdateEvent) -> Scene:
    # TODO: Might want to refactor the dialog system.
    pehter = update_event.scene._entity
    pehter.dialog_name = None
    pehter.dialog_options = []

    stanza = update_event.stanzas["pehter_nation"]
    next_scene = LocationScene(update_event.locations["alba"])
    return StanzaScene(stanza, next_scene)


def _pehter_family_callback_fn(update_event: UpdateEvent) -> Scene:
    # TODO: Might want to refactor the dialog system.
    pehter = update_event.scene._entity
    pehter.dialog_name = None
    pehter.dialog_options = []

    stanza = update_event.stanzas["pehter_family"]
    next_scene = LocationScene(update_event.locations["alba"])
    return StanzaScene(stanza, next_scene)


def _pehter_self_callback_fn(update_event: UpdateEvent) -> Scene:
    # TODO: Might want to refactor the dialog system.
    pehter = update_event.scene._entity
    pehter.dialog_name = None
    pehter.dialog_options = []

    stanza = update_event.stanzas["pehter_self"]
    return DialogScene(stanza, pehter)


def _iustitia_callback_fn(interact_event: InteractEvent) -> Scene:
    update_event = interact_event.update_event
    update_event.epic.hero.add_attribute("Fate Breaker")

    stanza = update_event.stanzas["iustitia_escape"]
    next_scene = LocationScene(update_event.locations["proto_imperion"])
    return StanzaScene(stanza, next_scene)


def make_inferno() -> Location:
    inferno_entities = [
        Person("Pehter",
               dialog_name="dialog/pehter",
               dialog_options=[
                    DialogOption("I came for my nation.",
                                 _pehter_nation_callback_fn),
                    DialogOption("I came for my family.",
                                 _pehter_family_callback_fn),
                    DialogOption("I came for myself.",
                                 _pehter_self_callback_fn),
               ]),
        Person("Iustitia",
               dialog_name="dialog/iustitia",
               callback_fn=_iustitia_callback_fn),
    ]

    return Location("Inferno", inferno_entities)
