from typing import Text


class UpdateEvent:

    def __init__(self, epic, last_scene, scenes):
        self.epic = epic
        self.last_scene = last_scene
        self._scenes = scenes

    def get_scene(self, name: Text):
    	return self._scenes.get(name, None)
