from abc import ABCMeta
from overrides import overrides
from typing import List, Text

from ..events import UpdateEvent


class Stanza(metaclass=ABCMeta):

    def generate(self, event: UpdateEvent, long_form=True, **kwargs):
        raise NotImplementedError


class TemplateStanza(Stanza):

    def __init__(self, lines: List[Text]):
        self._lines = lines

    @overrides
    def generate(self, event: UpdateEvent, long_form=True, **kwargs):
        return "\n".join(self._format(line, event, **kwargs)
                         for line in self._lines
                         if long_form or self._is_commented(line))

    @staticmethod
    def _format(line, event: UpdateEvent, **kwargs):
        # TODO: Should have the capability for conditionals and stuff.
        kwargs["HERO"] = event.epic.hero
        line = line[2:] if line.startswith("# ") else line
        return line.format(**kwargs).strip()

    @staticmethod
    def _is_commented(line):
        return line.startswith("# ")
