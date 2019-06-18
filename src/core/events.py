class UpdateEvent:

    def __init__(self,
                 epic,
                 scene,
                 last_scene,
                 scenes,
                 stanzas,
                 locations,
                 dialog_scene_type,
                 location_scene_type):
        self.epic = epic
        self.scene = scene
        self.last_scene = last_scene
        self.stanzas = stanzas
        self.scenes = scenes
        self.locations = locations
        # Need to pass these types to prevent module dependency issues when
        # dynamically constructing scenes.
        self.dialog_scene_type = dialog_scene_type
        self.location_scene_type = location_scene_type


class InteractEvent:

    def __init__(self, update_event, entity):
        self.update_event = update_event
        self.entity = entity


class CommandEvent:

    def __init__(self,
                 update_event,
                 cmd,
                 args,
                 cmd_mapping):
        self.update_event = update_event
        self.cmd = cmd
        self.args = args
        self.cmd_mapping = cmd_mapping
