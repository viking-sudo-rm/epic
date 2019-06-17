from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import InteractEvent
from src.core.location import Location, Sea
from src.core.scenes import LocationScene, Scene


def _make_ilion_duel_callback_fn(person: Text) -> Callable[[InteractEvent],
                                                           Scene]:
    def _ilion_duel_callback_fn(interact_event: InteractEvent) -> Scene:
        return interact_event.update_event.scenes["duel_" + person]
    return _ilion_duel_callback_fn


def _make_new_dock(sea: Sea) -> Object:
    def callback_fn(event: InteractEvent):
        event = event.update_event
        if event.scene is event.scenes["ilion"]:
            # If we are in the Ilion battle, do the escape scene.
            return event.scenes["sea_escape"]
        else:
            return LocationScene(sea)
    return Object("Dock", callback_fn=callback_fn)


def make_locations() -> Dict[Text, Location]:

    east_nostratic = Sea("East Nostratic Sea")
    west_nostratic = Sea("West Nostratic Sea")

    ilion_entities = [
        Person("Polypugnos",
               callback_fn=_make_ilion_duel_callback_fn("polypugnos")),
        Person("Nemeson",
               callback_fn=_make_ilion_duel_callback_fn("nemeson")),
        _make_new_dock(east_nostratic),
    ]

    karthago_entities = [
        Person("Maliket", dialog_name="dialog/maliket"),
        _make_new_dock(west_nostratic),
    ]

    ilion = Location("Ilion", ilion_entities)
    karthago = Location("Karthago", karthago_entities)
    medinta_baal = Location("Medinta Baal", [_make_new_dock(east_nostratic)])
    os_aegypta = Location("Os Aegypta", [_make_new_dock(east_nostratic)])

    # TODO: Allow going back to ruined Ilion?
    # east_nostratic.north_neighbor = ilion
    east_nostratic.west_neighbor = west_nostratic
    east_nostratic.east_neighbor = medinta_baal
    east_nostratic.south_neighbor = os_aegypta
    west_nostratic.east_neighbor = east_nostratic
    west_nostratic.south_neighbor = karthago

    # TODO: Have ports/islands in the seas? Cyclops battle.

    return {
        "ilion": ilion,
        "karthago": karthago,
        "east_nostratic": east_nostratic,
        "west_nostratic": west_nostratic,
    }
