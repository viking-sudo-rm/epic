class Location:

    """Class containing characters, buildings, etc."""

    def __init__(self, placename, entities=[]):
        self.placename = placename
        self._entities = entities

    def update(self, event):
        pass


class Entity:

    """A person or object in the world."""

    def __init__(self, name, position=None):
        self.name = name
        self.position = position

    def __repr__(self):
        return "Entity(%s)" % self.name
