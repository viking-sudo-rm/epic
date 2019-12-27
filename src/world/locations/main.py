from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import InteractEvent, UpdateEvent
from src.core.interface.dialog import DialogOption
from src.core.location import Location, Sea
from src.core.scenes.base import Scene
from src.core.scenes.dialog import DialogScene
from src.core.scenes.location import LocationScene
from src.core.scenes.stanza import StanzaScene

from src.world.locations.ilion import make_ilion
from src.world.locations.karthago import make_karthago
from src.world.locations.cimmeria import make_cimmeria
from src.world.locations.inferno import make_inferno

from src.world.locations.utils import make_new_dock


def make_locations() -> Dict[Text, Location]:

    # TODO: Add "dock <port>" command to enter ports from the sea. This allows
    # allowing each sea to have multiple ports (a list which appears to the
    # player).
    east_nostratic = Sea("East Nostratic Sea")
    west_nostratic = Sea("West Nostratic Sea")
    east_nostratic.west_neighbor = west_nostratic
    west_nostratic.east_neighbor = east_nostratic

    medinta_baal = Location("Medinta Baal", [make_new_dock(east_nostratic)])
    os_aegypta = Location("Os Aegypta", [make_new_dock(east_nostratic)])
    inferno = make_inferno()
    alba = Location("Alba", [])
    proto_imperion = Location("Proto Imperion", [])

    east_nostratic.east_neighbor = medinta_baal
    east_nostratic.south_neighbor = os_aegypta

    # TODO: Have ports/islands in the seas? Cyclops battle.
    # TODO: Need to go to cyclops island to upgrade ship before going further.

    return {
        "east_nostratic": east_nostratic,
        "west_nostratic": west_nostratic,
        "ilion": make_ilion(east_nostratic),
        "karthago": make_karthago(west_nostratic),
        "medinta_baal": medinta_baal,
        "os_aegypta": os_aegypta,
        "cimmeria": make_cimmeria(west_nostratic),
        "inferno": inferno,
        "alba": alba,
        "proto_imperion": proto_imperion,
    }
