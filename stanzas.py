from abc import ABCMeta

from events import UpdateEvent
from utils import overrides


class Stanza(metaclass=ABCMeta):

    def generate(self, event:UpdateEvent, **kwargs):
        raise NotImplementedError


class TemplateStanza(Stanza):

    def __init__(self, text):
        self._text = text

    @overrides(Stanza)
    def generate(self, event: UpdateEvent, **kwargs):
        # TODO: Should have capability for conditionals and stuff.
        kwargs["HERO"] = event.epic.hero.name if event.epic.hero is not None else "Anon"
        return self._text.format(**kwargs).strip()
