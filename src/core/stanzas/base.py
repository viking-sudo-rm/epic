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
                         if self._fits_form(line, long_form))

    @staticmethod
    def _format(line, event: UpdateEvent, **kwargs):
        # TODO: Should have the capability for conditionals and stuff.
        kwargs["HERO"] = event.epic.hero
        line = TemplateStanza._remove_comments(line)
        return line.format(**kwargs).strip()

    @staticmethod
    def _remove_comments(line):
        if line.startswith("# ") or line.startswith("! "):
            return line[2:]
        else:
            return line

    @staticmethod
    def _fits_form(line, long_form):
        if not long_form and line.startswith("# "):
            return False
        elif long_form and line.startswith("! "):
            return False
        else:
            return True
