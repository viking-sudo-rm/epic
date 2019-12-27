from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import InteractEvent, UpdateEvent
from src.core.interface.dialog import DialogOption
from src.core.location import Location, Sea
from src.core.scenes.base import Scene
from src.core.scenes.dialog import DialogScene
from src.core.scenes.location import LocationScene
from src.core.scenes.stanza import StanzaScene
from src.world.locations.utils import make_new_dock


def _sybil_callback_fn(interact_event: InteractEvent) -> Scene:
    # TODO: Sybil raps?
    update_event = interact_event.update_event
    if "Widower" in update_event.epic.hero.attributes:
        stanza = update_event.stanzas["sybil_underworld"]
        next_scene = LocationScene(update_event.locations["inferno"])
        return StanzaScene(stanza, next_scene)
    else:
        stanza = update_event.stanzas["sybil_denial"]
        return DialogScene(stanza, interact_event.entity)


def make_cimmeria(seas: Dict[str, Sea]) -> Location:
    west_nostratic = seas["west_nostratic"]

    cimmeria_entities = [
        Person("Sybil",
               dialog_name="dialog/sybil",
               callback_fn=_sybil_callback_fn),
        make_new_dock(west_nostratic),
    ]

    cimmeria = Location("Cimmeria", cimmeria_entities)
    west_nostratic.north_neighbor = cimmeria
    return cimmeria
