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


def make_os_aegypta(seas: Dict[str, Sea]) -> Location:
    east_nostratic = seas["east_nostratic"]
    os_aegypta = Location("Os Aegypta", [make_new_dock(east_nostratic)])
    east_nostratic.south_neighbor = os_aegypta
    return os_aegypta
