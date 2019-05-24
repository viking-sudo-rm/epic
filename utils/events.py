from typing import Text
import random


class UpdateEvent:

    def __init__(self, epic, scene, last_scene, scenes, stanzas):
        self.epic = epic
        self.scene = scene
        self.last_scene = last_scene
        self.stanzas = stanzas
        self._scenes = scenes

    def get_scene(self, name):
    	"""Either takes a function which returns a scene name, or a scene name."""
    	if callable(name):
    		name = name(self)
    	return self._scenes.get(name, None)
