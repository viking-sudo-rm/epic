from typing import Dict, List, Text

from src.core.events import UpdateEvent
from src.core.entities import Person
from src.core.location import Location
from src.core.scenes.base import Scene
from src.core.scenes.duel import DuelScene
from src.core.scenes.location import LocationScene
from src.core.scenes.selection import SelectionScene
from src.core.scenes.stanza import StanzaScene
from src.core.stanzas.base import Stanza


def make_scenes(stanzas: Dict[Text, Stanza],
                heroes: List[Person],
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
                                      heroes,
                                      lambda hero: hero.name.lower(),
                                      lambda epic: epic.set_hero,
                                      next_scene="ilion"),
        "ilion": LocationScene(locations["ilion"], stanzas["enter_ilion"]),

        # Defend Ilion.
        "duel_polypugnos": DuelScene(locations["ilion"]._entities[0],
                                     next_scene=_ilion_duel_scene_selector),
        "duel_nemeson": DuelScene(locations["ilion"]._entities[1],
                                  next_scene=_ilion_duel_scene_selector),
        "defended_ilion": LocationScene(locations["ilion"],
                                        stanzas["defended_ilion"],
                                        always_announce=True),
    }
    return scenes["muse"], scenes
