from typing import Text

class Epic:

    def __init__(self):
        self._stanzas = []
        self.hero = None

    def add_stanza(self, stanza: Text):
        self._stanzas.append(stanza)

    @property
    def story(self):
        return "\n\n".join(self._stanzas)

    def set_hero(self, hero):
        self.hero = hero


class GameState:

    def __init__(self, epic, scene, world):
        self.epic = epic
        self.scene = scene
        self.world = world

    # @classmethod
    # def create_fresh(cls):
    #     game_state = cls()