class UpdateEvent:

    def __init__(self, epic, scene, last_scene, scenes, stanzas):
        self.epic = epic
        self.scene = scene
        self.last_scene = last_scene
        self.stanzas = stanzas
        self.scenes = scenes


class InteractEvent:

    def __init__(self, update_event, entity):
        self.update_event = update_event
        self.entity = entity
