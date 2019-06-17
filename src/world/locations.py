from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import InteractEvent
from src.core.location import Location, Sea
from src.core.scenes import LocationScene, Scene, StanzaScene


def _make_ilion_duel_callback_fn(person: Text) -> Callable[[InteractEvent],
                                                           Scene]:
    def _ilion_duel_callback_fn(interact_event: InteractEvent) -> Scene:
        return interact_event.update_event.scenes["duel_" + person]
    return _ilion_duel_callback_fn


def _make_new_dock(sea: Sea) -> Object:
    def callback_fn(interact_event: InteractEvent):
        event = interact_event.update_event
        next_scene = LocationScene(sea)
        if event.scene is event.scenes["ilion"]:
            # If we are in the Ilion battle, do the escape scene.
            stanza = event.stanzas["sea_escape"]
            return StanzaScene(stanza, next_scene)
        elif isinstance(event.scene, LocationScene):
            # If we're ditching Maliket, kill her.
            maliket = event.scene.location.get_entity("Maliket")
            if maliket is not None and maliket.lover is event.epic.hero:
                maliket.kill()
                stanza = event.stanzas["maliket_suicide"]
                return StanzaScene(stanza, next_scene)
        return next_scene
    return Object("Dock", callback_fn=callback_fn)


def _maliket_callback_fn(interact_event: InteractEvent):
    interact_event.entity.lover = interact_event.update_event.epic.hero
    stanza = interact_event.update_event.stanzas["maliket_cave"]
    next_scene = LocationScene(interact_event.entity.location)
    return StanzaScene(stanza, next_scene)


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
        Person("Maliket",
               dialog_name="dialog/maliket",
               callback_fn=_maliket_callback_fn),
        _make_new_dock(west_nostratic),
    ]

    ilion = Location("Ilion", ilion_entities)
    karthago = Location("Karthago", karthago_entities)
    medinta_baal = Location("Medinta Baal", [_make_new_dock(east_nostratic)])
    os_aegypta = Location("Os Aegypta", [_make_new_dock(east_nostratic)])

    # TODO: Close ports in Ilion/Karthago?
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
