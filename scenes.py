from typing import Dict, Text

from heroes import make_heroes

from utils.events import UpdateEvent
from utils.location import Location
from utils.scenes import DuelScene, LocationScene, Scene, SelectionScene
from utils.scenes import StanzaScene
from utils.stanzas.base import Stanza


def make_scenes(stanzas: Dict[Text, Stanza],
                locations: Dict[Text, Location]) -> Scene:

    def _ilion_duel_scene_selector(event: UpdateEvent) -> Text:
        ilion = event.scene.location
        if len(ilion._entities) > 1:
            return "ilion"
        else:
            return "defended_ilion"

    scenes = {
        # Intro sequence.
        "muse": StanzaScene(stanzas["muse"], next_scene="select_hero"),
        "select_hero": SelectionScene("Choose Hero:",
                                      make_heroes(),
                                      lambda hero: hero.name.lower(),
                                      lambda epic: epic.set_hero,
                                      next_scene="ilion"),
        "ilion": LocationScene(locations["ilion"], stanzas["enter_ilion"]),

        # Run away.
        "sea_escape": StanzaScene(stanzas["sea_escape"], next_scene="sea"),

        # Defend Ilion.
        "duel_polypugnos": DuelScene(locations["ilion"]._entities[0],
                                     next_scene=_ilion_duel_scene_selector),
        "duel_nemeson": DuelScene(locations["ilion"]._entities[1],
                                  next_scene=_ilion_duel_scene_selector),
        "defended_ilion": LocationScene(locations["ilion"],
                                        stanzas["defended_ilion"]),
    }
    return scenes["muse"], scenes
