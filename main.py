import os
from typing import Dict, Text

from src.core.epic import Epic
from src.core.events import UpdateEvent
from src.core.scenes.dialog import DialogScene
from src.core.scenes.location import LocationScene
from src.core.stanzas.base import Stanza, TemplateStanza
from src.world.heroes import make_heroes
from src.world.locations import make_locations
from src.world.scenes import make_scenes


def load_stanzas() -> Dict[Text, Stanza]:
    stanzas = {}
    for root, dirs, files in os.walk("texts"):
        for file in files:
            path = root + "/" + file  # This is easier than using variable sep.
            # path = os.path.join(root, file)
            with open(path) as fh:
                stanza = TemplateStanza(fh.readlines())
                key = path[6:].replace(".txt", "")
                stanzas[key] = stanza
    return stanzas


def main():
    stanzas = load_stanzas()
    heroes = make_heroes()
    locations = make_locations()
    scene, scenes = make_scenes(stanzas, heroes, locations)
    last_scene = None
    epic = Epic()

    while scene is not None:
        update_event = UpdateEvent(epic, scene, last_scene, scenes, stanzas,
                                   locations, DialogScene, LocationScene)
        last_scene = scene
        scene = scene.update(update_event)

    print("=" * 30, "EPIC", "=" * 30)
    print(epic.story)


if __name__ == "__main__":
    main()
