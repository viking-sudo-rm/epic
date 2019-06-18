from typing import List

from src.core.entities import Person, Pronoun


def make_heroes() -> List[Person]:
    return [
        Person("Aeneas", attributes=["Pious", "Boring"]),
        Person("Dido",
               attributes=["Burning", "Vengeful"],
               pronoun=Pronoun.FEMININE),
        Person("Beowulf", attributes=["Adventurer", "Loyal"]),
    ]
