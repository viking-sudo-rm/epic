import scenes
from epic import Epic
from location import Location, Entity


def make_scene():
    rome = Location("Rome", [Entity(name) for name in ["Romulus", "Remus"]])
    scene = scenes.LocationScene(rome)
    # TODO: These should be Hero instances; maybe unify Entity and Hero?
    scene = scenes.SelectionScene(scene, "Choose Character:", [Entity(name) for name in ["Aeneas", "Dido", "Beowulf"]], lambda epic: epic.set_character)
    scene = scenes.TextScene(scene, "Hello world")


def main():
    scene = make_scene()
    last_scene = None
    epic = Epic()

    while scene is not None:
        update_event = scenes.UpdateEvent(epic, last_scene)
        last_scene = scene
        scene = scene.update(update_event)

    print("=" * 30, "EPIC", "=" * 30)
    print(epic.story)


if __name__ == "__main__":
    main()
