from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import InteractEvent, UpdateEvent
from src.core.interface.dialog import DialogOption
from src.core.location import Location, Sea
from src.core.scenes.base import Scene
from src.core.scenes.dialog import DialogScene
from src.core.scenes.end import EndScene
from src.core.scenes.location import LocationScene
from src.core.scenes.stanza import StanzaScene
from src.world.locations.utils import make_new_dock


def _brutus_callback_fn(interact_event: InteractEvent) -> Scene:
    ending = EndScene("hello", None)
    brutus = interact_event.update_event.locations["ilion"]._entities[1]
    return DuelScene(brutus, next_scene=ending)


def make_alba() -> Location:

    alba_entities = [
        Person("Calida",
               dialog_name="dialog/calida"),
        Person("Brutus",
               dialog_name="dialog/brutus",
               callback_fn=_brutus_callback_fn),
    ]

    return Location("Alba", alba_entities)
