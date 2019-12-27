from typing import Callable, Dict, Text

from src.core.entities import Object, Person
from src.core.events import InteractEvent, UpdateEvent
from src.core.interface.dialog import DialogOption
from src.core.location import Location, Sea
from src.core.scenes.base import Scene
from src.core.scenes.dialog import DialogScene
from src.core.scenes.location import LocationScene
from src.core.scenes.stanza import StanzaScene


def make_new_dock(sea: Sea) -> Object:
    def callback_fn(interact_event: InteractEvent):
        event = interact_event.update_event
        next_scene = LocationScene(sea)
        if event.scene is event.scenes["ilion"]:
            # If we are in the Ilion battle, do the escape scene.
            stanza = event.stanzas["sea_escape"]
            return StanzaScene(stanza, next_scene)
        elif isinstance(event.scene, LocationScene):
            # If we're ditching Maliket, kill her.
            maliket = event.scene.location.get_entity("Maliket")
            if maliket is not None and maliket.lover is event.epic.hero:
                maliket.kill()
                event.epic.hero.add_attribute("Widower")
                stanza = event.stanzas["maliket_suicide"]
                return StanzaScene(stanza, next_scene)
        return next_scene
    return Object("Dock", callback_fn=callback_fn)
