from typing import List, Text

from .entities import Entity
from .events import UpdateEvent


class Location:

    """Class containing characters, buildings, etc."""

    def __init__(self,
                 placename: Text,
                 entities: List[Entity] = []):
        self.placename = placename
        self._entities = entities
        self.first_visit = True
        for entity in self._entities:
            entity.location = self

    def get_entity(self, name: Text) -> Entity:
        # TODO: Might want to change implementation of self._entities.
        name_predicate = lambda entity: entity.name == name
        results = filter(name_predicate, self._entities)
        return results[0] if len(results) > 0 else None

    def remove_entity(self, entity: Entity):
        self._entities.remove(entity)

    def update(self, event: UpdateEvent):
        pass


class Sea(Location):

    """A Location from which we can sail to other locations."""

    def __init__(self,
                 placename: Text,
                 entities: List[Entity] = [],
                 north_neighbor: Location = None,
                 east_neighbor: Location = None,
                 south_neighbor: Location = None,
                 west_neighbor: Location = None):
        super().__init__(placename, entities)
        self.north_neighbor = north_neighbor
        self.east_neighbor = east_neighbor
        self.south_neighbor = south_neighbor
        self.west_neighbor = west_neighbor
