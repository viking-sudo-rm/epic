from overrides import overrides
from typing import Any, Callable, List, Text

from .base import NextSceneType, Scene
from ..epic import Epic
from ..events import UpdateEvent


class SelectionScene(Scene):
    """Choose a character at the beginning."""

    def __init__(self,
                 prompt: Text,
                 options: List[Any],
                 value_fn: Callable[[Any], Text],
                 select_fn: Callable[[Epic], Callable[[Any], None]],
                 next_scene: NextSceneType):
        self._next_scene = next_scene
        self._prompt = prompt
        self._options = options
        self._value_fn = value_fn
        self._select_fn = select_fn

    @overrides
    def update(self, event: UpdateEvent) -> Scene:
        print("=" * 10, "SELECTION", "=" * 10)
        print(self._prompt, self._options)
        query = input("Select: ").lower()
        for option in self._options:
            if query == self._value_fn(option):
                selection = option
                break
        self._select_fn(event.epic)(selection)
        stanza_name = "select/" + self._value_fn(selection)
        if stanza_name in event.stanzas:
            text = event.stanzas[stanza_name].generate(event)
            print(text)
            input()
            event.epic.add_stanza(text)
        return self.get_scene(self._next_scene, event)
