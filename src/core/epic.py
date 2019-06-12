from typing import Text


class Epic:

    # TODO: Might want to encapsulate this stuff in GameState or something.

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
