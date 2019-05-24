from typing import List, Text

from .entities import Entity
from .events import UpdateEvent

class Location:

    """Class containing characters, buildings, etc."""

    def __init__(self, placename: Text, entities: List[Entity] = []):
        self.placename = placename
        self._entities = entities
        for entity in self._entities:
        	entity.location = self

    def get_entity(self, name: Text) -> Entity:
    	# TODO: Might want to change implementation of self._entities.
    	for entity in self._entities:
    		if entity.name == "name":
    			return entity
    	return None

    def remove_entity(self, entity: Entity):
    	self._entities.remove(entity)

    def update(self, event: UpdateEvent):
        pass
