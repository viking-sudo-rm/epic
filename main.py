import os
from typing import Dict, List, Text

from entities import Entity, Person, Object
from epic import Epic
from events import UpdateEvent
from location import Location
from scenes import LocationScene, Scene, SelectionScene, StanzaScene
from stanzas import Stanza, TemplateStanza


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

    def _dock_callback_fn(event: UpdateEvent) -> Scene:
        return event.get_scene("sea_escape")

    return {
        "ilion": Location("Ilion", [
            Person("Polypugnos"),
            Person("Nemeson"),
            Object("Dock", callback_fn=_dock_callback_fn),
        ]),
    }


def make_scenes(stanzas: Dict[Text, Stanza], locations: Dict[Text, Location]) -> Scene:
    scenes = {
        "muse": StanzaScene(stanzas["muse"], next_scene="select_hero"),
        "select_hero": SelectionScene("Choose Hero:",
                                      [Entity(name) for name in ["Aeneas", "Dido", "Beowulf"]],
                                      lambda hero: hero.name.lower(),
                                      lambda epic: epic.set_hero,
                                      stanzas,
                                      next_scene="ilion"),
        "ilion": LocationScene(locations["ilion"], stanzas["enter_city"]),
        "sea_escape": StanzaScene(stanzas["sea_escape"], next_scene="sea"),
    }
    return scenes["muse"], scenes


def main():
    stanzas = load_stanzas()
    locations = make_locations()
    scene, scenes = make_scenes(stanzas, locations)
    last_scene = None
    epic = Epic()

    while scene is not None:
        update_event = UpdateEvent(epic, last_scene, scenes)
        last_scene = scene
        scene = scene.update(update_event)

    print("=" * 30, "EPIC", "=" * 30)
    print(epic.story)


if __name__ == "__main__":
    main()
