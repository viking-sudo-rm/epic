from enum import Enum


class Pronoun(Enum):

    MASCULINE = ("he", "him", "his")
    FEMININE = ("she", "her", "her")

    def __init__(self, nom, acc, gen):
        self.nom = nom
        self.acc = acc
        self.gen = gen

    @property
    def title_nom(self):
        return self.nom.title()

    @property
    def title_acc(self):
        return self.acc.title()

    @property
    def title_gen(self):
        return self.gen.title()
