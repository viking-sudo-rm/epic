import os
from typing import Dict, List, Text

from events import UpdateEvent
import scenes
from stanzas import Stanza, TemplateStanza
from epic import Epic
from location import Location
from entities import Entity, Person, Object


def load_stanzas() -> Dict[Text, Stanza]:
    stanzas = {}
    for root, dirs, files in os.walk("texts"):
        for file in files:
            path = os.path.join(root, file)
            with open(path) as fh:
                stanza = TemplateStanza(fh.read())
                stanzas[file.replace(".txt", "")] = stanza
    return stanzas


def make_locations() -> Dict[Text, Location]:
    return {
        "ilion": Location("Ilion", [
            Person("Polypugnos"),
            Person("Nemeson"),
            Object("Dock", callback_fn=lambda event: print("We at the dock!")),
            ]),
    }


# TODO: Save locations in JSON (default and saved world).
# TODO: Also save scene graph in JSON.


def make_scene_graph(stanzas, locations) -> scenes.Scene:
    scene = scenes.LocationScene(locations["ilion"], stanzas["enter_city"])
    scene = scenes.SelectionScene(scene, "Choose Hero:",
                                  [Entity(name) for name in ["Aeneas", "Dido", "Beowulf"]],
                                  lambda hero: hero.name.lower(),
                                  lambda epic: epic.set_hero,
                                  stanzas)
    scene = scenes.StanzaScene(scene, stanzas["muse"])
    return scene


def main():
    stanzas = load_stanzas()
    locations = make_locations()
    scene = make_scene_graph(stanzas, locations)
    last_scene = None
    epic = Epic()

    while scene is not None:
        update_event = UpdateEvent(epic, last_scene)
        last_scene = scene
        scene = scene.update(update_event)

    print("=" * 30, "EPIC", "=" * 30)
    print(epic.story)


if __name__ == "__main__":
    main()
