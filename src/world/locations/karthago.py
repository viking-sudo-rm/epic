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


def _maliket_callback_fn(interact_event: InteractEvent) -> Scene:
    interact_event.entity.lover = interact_event.update_event.epic.hero
    stanza = interact_event.update_event.stanzas["maliket_cave"]
    next_scene = LocationScene(interact_event.entity.location)
    return StanzaScene(stanza, next_scene)


def make_karthago(seas: Dict[str, Sea]) -> Location:
    west_nostratic = seas["west_nostratic"]

    karthago_entities = [
        Person("Maliket",
               dialog_name="dialog/maliket",
               callback_fn=_maliket_callback_fn),
        make_new_dock(west_nostratic),
    ]

    karthago = Location("Karthago", karthago_entities)
    west_nostratic.south_neighbor = karthago
    return karthago
