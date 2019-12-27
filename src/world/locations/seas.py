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


def make_seas() -> Dict[str, Sea]:
    # TODO: Add "dock <port>" command to enter ports from the sea. This allows
    # allowing each sea to have multiple ports (a list which appears to the
    # player).
    east_nostratic = Sea("East Nostratic Sea")
    west_nostratic = Sea("West Nostratic Sea")
    east_nostratic.west_neighbor = west_nostratic
    west_nostratic.east_neighbor = east_nostratic

    return {
      "east_nostratic": east_nostratic,
      "west_nostratic": west_nostratic,
    }
