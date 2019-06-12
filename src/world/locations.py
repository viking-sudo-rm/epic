from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import UpdateEvent
from src.core.location import Location
from src.core.scenes import Scene


def make_locations() -> Dict[Text, Location]:

    def _dock_callback_fn(event: UpdateEvent) -> Scene:
        if event.scene is event._scenes["ilion"]:
            return event.get_scene("sea_escape")
        else:
            print("The dock is pretty boring.")

    def _make_ilion_duel_callback_fn(person: Text) -> Callable[[UpdateEvent],
                                                               Scene]:
        def _ilion_duel_callback_fn(event: UpdateEvent) -> Scene:
            return event.get_scene("duel_" + person)
        return _ilion_duel_callback_fn

    return {
        "ilion": Location("Ilion", [
            Person("Polypugnos",
                   callback_fn=_make_ilion_duel_callback_fn("polypugnos")),
            Person("Nemeson",
                   callback_fn=_make_ilion_duel_callback_fn("nemeson")),
            Object("Dock", callback_fn=_dock_callback_fn),
        ]),
    }
