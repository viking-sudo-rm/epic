from abc import ABCMeta
from overrides import overrides
from typing import Text

from ..events import UpdateEvent


class Stanza(metaclass=ABCMeta):

    def generate(self, event:UpdateEvent, **kwargs):
        raise NotImplementedError


class TemplateStanza(Stanza):

    def __init__(self, text: Text):
        self._text = text

    @overrides
    def generate(self, event: UpdateEvent, **kwargs):
        # TODO: Should have capability for conditionals and stuff.
        kwargs["HERO"] = event.epic.hero.name if event.epic.hero is not None else "Anon"
        return self._text.format(**kwargs).strip()

# TODO: Should mark whether stanza should be included at play time or not.
