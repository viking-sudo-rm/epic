import os
from typing import Callable, Dict, List, Text

from utils.entities import Entity, Person, Object
from utils.epic import Epic
from utils.events import UpdateEvent
from utils.location import Location
from utils.scenes import DuelScene, LocationScene, Scene, SelectionScene, StanzaScene
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


def make_locations() -> Dict[Text, Location]:

    def _dock_callback_fn(event: UpdateEvent) -> Scene:
        if event.scene is event._scenes["ilion"]:
            return event.get_scene("sea_escape")
        else:
            print("The dock is pretty boring.")

    def _make_ilion_duel_callback_fn(person: Text) -> Callable[[UpdateEvent], Scene]:
        def _ilion_duel_callback_fn(event: UpdateEvent) -> Scene:
            return event.get_scene("duel_" + person)
        return _ilion_duel_callback_fn

    return {
        "ilion": Location("Ilion", [
            Person("Polypugnos", callback_fn=_make_ilion_duel_callback_fn("polypugnos")),
            Person("Nemeson", callback_fn=_make_ilion_duel_callback_fn("nemeson")),
            Object("Dock", callback_fn=_dock_callback_fn),
        ]),
    }


def make_scenes(stanzas: Dict[Text, Stanza], locations: Dict[Text, Location]) -> Scene:

    def _ilion_duel_next_scene_selector(event: UpdateEvent) -> Text:
        ilion = event.scene.location
        if len(ilion._entities) > 1:
            return "ilion"
        else:
            return "defended_ilion"

    scenes = {
        # Intro sequence.
        "muse": StanzaScene(stanzas["muse"], next_scene="select_hero"),
        "select_hero": SelectionScene("Choose Hero:",
                                      [Entity(name) for name in ["Aeneas", "Dido", "Beowulf"]],
                                      lambda hero: hero.name.lower(),
                                      lambda epic: epic.set_hero,
                                      next_scene="ilion"),
        "ilion": LocationScene(locations["ilion"], stanzas["enter_ilion"]),

        # Run away.
        "sea_escape": StanzaScene(stanzas["sea_escape"], next_scene="sea"),

        # Defend Ilion.
        "duel_polypugnos": DuelScene(locations["ilion"]._entities[0], next_scene=_ilion_duel_next_scene_selector),
        "duel_nemeson": DuelScene(locations["ilion"]._entities[1], next_scene=_ilion_duel_next_scene_selector),
        "defended_ilion": LocationScene(locations["ilion"], stanzas["defended_ilion"]),
    }
    return scenes["muse"], scenes


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
