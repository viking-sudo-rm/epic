from abc import ABCMeta

from utils import overrides


class Stanza(metaclass=ABCMeta):

    def generate(self):
        # TODO: This should take a bunch of arguments that can be done.
        raise NotImplementedError("generate not implemented.")


class TemplateStanza(Stanza):

    def __init__(self, text):
        self._text = text

    @overrides(Stanza)
    def generate(self):
        return text
