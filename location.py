from typing import List

from entities import Entity
from events import UpdateEvent

class Location:

    """Class containing characters, buildings, etc."""

    def __init__(self, placename, entities: List[Entity] = []):
        self.placename = placename
        self._entities = entities

    def update(self, event: UpdateEvent):
        pass
