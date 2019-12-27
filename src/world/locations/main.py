from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import InteractEvent, UpdateEvent
from src.core.interface.dialog import DialogOption
from src.core.location import Location, Sea
from src.core.scenes.base import Scene
from src.core.scenes.dialog import DialogScene
from src.core.scenes.location import LocationScene
from src.core.scenes.stanza import StanzaScene

from src.world.locations.seas import make_seas
from src.world.locations.ilion import make_ilion
from src.world.locations.karthago import make_karthago
from src.world.locations.cimmeria import make_cimmeria
from src.world.locations.inferno import make_inferno
from src.world.locations.alba import make_alba
from src.world.locations.medinta_baal import make_medinta_baal
from src.world.locations.os_aegypta import make_os_aegypta

from src.world.locations.utils import make_new_dock


def make_locations() -> Dict[Text, Location]:
    seas = make_seas()

    # TODO: Should we even have proto imperion here?
    proto_imperion = Location("Proto Imperion", [])

    # TODO: Have ports/islands in the seas? Cyclops battle.
    # TODO: Need to go to cyclops island to upgrade ship before going further.

    return {
        "east_nostratic": seas["east_nostratic"],
        "west_nostratic": seas["west_nostratic"],
        "ilion": make_ilion(seas),
        "karthago": make_karthago(seas),
        "medinta_baal": make_medinta_baal(seas),
        "os_aegypta": make_os_aegypta(seas),
        "cimmeria": make_cimmeria(seas),
        "inferno": make_inferno(),
        "alba": make_alba(),
        "proto_imperion": proto_imperion,
    }
