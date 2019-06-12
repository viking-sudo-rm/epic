from typing import List

from src.core.entities import Person, Pronoun


def make_heroes() -> List[Person]:
    return [
        Person("Aeneas"),
        Person("Dido", pronoun=Pronoun.FEMININE),
        Person("Beowulf"),
    ]
