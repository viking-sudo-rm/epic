class Epic:

    def __init__(self):
        self._stanzas = []
        self._character = None

    def add_stanza(self, stanza):
        self._stanzas.append(stanza)

    @property
    def story(self):
        return "\n\n".join(self._stanzas)

    def set_character(self, character):
        self._character = character


class GameState:

    def __init__(self, epic, scene, world):
        self.epic = epic
        self.scene = scene
        self.world = world

    # @classmethod
    # def create_fresh(cls):
    #     game_state = cls()