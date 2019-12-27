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


def _make_ilion_duel_callback_fn(person: Text) -> Callable[[InteractEvent],
                                                           Scene]:
    def _ilion_duel_callback_fn(interact_event: InteractEvent) -> Scene:
        return interact_event.update_event.scenes["duel_" + person]
    return _ilion_duel_callback_fn


def make_ilion(east_nostratic: Sea) -> Location:

    ilion_entities = [
        Person("Polypugnos",
               callback_fn=_make_ilion_duel_callback_fn("polypugnos")),
        Person("Nemeson",
               callback_fn=_make_ilion_duel_callback_fn("nemeson")),
        make_new_dock(east_nostratic),
    ]

    return Location("Ilion", ilion_entities)
