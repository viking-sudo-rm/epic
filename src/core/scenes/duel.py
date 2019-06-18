from overrides import overrides
import random

from .base import NextSceneType, Scene
from ..entities import Entity
from ..events import UpdateEvent


class DuelScene(Scene):

    def __init__(self, enemy: Entity, next_scene: NextSceneType):
        self._enemy = enemy
        self._next_scene = next_scene

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "DUEL", "=" * 10)
        print(event.epic.hero, "versus", self._enemy)
        input()
        self._enemy.kill()
        text = self.get_stock_duel_text(event)
        event.epic.add_stanza(text)
        print(text)
        return self.get_scene(self._next_scene, event)

    def get_stock_duel_text(self, event, weapon="lance"):
        """Return stock duel text picked randomly from duel stanzas."""
        num_duels = sum(1 for name in event.stanzas
                        if name.startswith("duels/stock"))
        duel_idx = random.randint(0, num_duels - 1)
        stanza = event.stanzas["duels/stock%d" % duel_idx]
        return stanza.generate(event,
                               ENEMY=self._enemy,
                               WEAPON=weapon)

    @property
    def location(self):
        return self._enemy.location
