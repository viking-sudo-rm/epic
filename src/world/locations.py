from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import UpdateEvent
from src.core.location import Location, Sea
from src.core.scenes import Scene


def make_locations() -> Dict[Text, Location]:

    def _dock_callback_fn(event: UpdateEvent) -> Scene:
        if event.scene is event.scenes["ilion"]:
            return event.scenes["sea_escape"]
        else:
            print("The dock is pretty boring.")

    def _make_ilion_duel_callback_fn(person: Text) -> Callable[[UpdateEvent],
                                                               Scene]:
        def _ilion_duel_callback_fn(event: UpdateEvent) -> Scene:
            return event.scenes["duel_" + person]
        return _ilion_duel_callback_fn

    ilion_entities = [
        Person("Polypugnos",
               callback_fn=_make_ilion_duel_callback_fn("polypugnos")),
        Person("Nemeson",
               callback_fn=_make_ilion_duel_callback_fn("nemeson")),
        Object("Dock", callback_fn=_dock_callback_fn),
    ]

    ilion = Location("Ilion", ilion_entities)
    carthage = Location("Carthage")

    east_nostratic = Sea("East Nostratic Sea")
    west_nostratic = Sea("West Nostratic Sea")

    # TODO: Allow going back to ruined Ilion?
    # east_nostratic.north_neighbor = ilion
    east_nostratic.west_neighbor = west_nostratic
    west_nostratic.east_neighbor = east_nostratic
    west_nostratic.south_neighbor = carthage

    return {
        "ilion": ilion,
        "carthage": carthage,
        "east_nostratic": east_nostratic,
        "west_nostratic": west_nostratic,
    }
