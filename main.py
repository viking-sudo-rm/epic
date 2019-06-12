import os
from typing import Dict, Text

from locations import make_locations
from scenes import make_scenes

from utils.epic import Epic
from utils.events import UpdateEvent
from utils.stanzas.base import Stanza, TemplateStanza


def load_stanzas() -> Dict[Text, Stanza]:
    stanzas = {}
    for root, dirs, files in os.walk("texts"):
        for file in files:
            path = os.path.join(root, file)
            with open(path) as fh:
                stanza = TemplateStanza(fh.read())
                key = path[6:].replace(".txt", "")
                stanzas[key] = stanza
    return stanzas


def main():
    stanzas = load_stanzas()
    locations = make_locations()
    scene, scenes = make_scenes(stanzas, locations)
    last_scene = None
    epic = Epic()

    while scene is not None:
        update_event = UpdateEvent(epic, scene, last_scene, scenes, stanzas)
        last_scene = scene
        scene = scene.update(update_event)

    print("=" * 30, "EPIC", "=" * 30)
    print(epic.story)


if __name__ == "__main__":
    main()
