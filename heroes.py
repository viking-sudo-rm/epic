from typing import List

from utils.entities import Person, Pronoun


def make_heroes() -> List[Person]:
    return [
        Person("Aeneas"),
        Person("Dido", Pronoun.FEMININE),
        Person("Beowulf"),
    ]
