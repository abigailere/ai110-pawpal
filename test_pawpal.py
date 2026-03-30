from pawpal_system import Task, Pet


def test_add_task():
    pet = Pet(name="Buddy", species="dog")
    task = Task(title="Walk", duration=30, priority="high")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Walk"
    assert pet.tasks[0].pet_name == "Buddy"
    print("test_add_task passed")


def test_remove_task():
    pet = Pet(name="Buddy", species="dog")
    task = Task(title="Walk", duration=30, priority="high")
    pet.add_task(task)

    pet.remove_task("Walk")

    assert len(pet.tasks) == 0
    print("test_remove_task passed")


def test_remove_nonexistent_task():
    pet = Pet(name="Buddy", species="dog")
    task = Task(title="Walk", duration=30, priority="high")
    pet.add_task(task)

    pet.remove_task("Bath")  # doesn't exist

    assert len(pet.tasks) == 1  # Walk should still be there
    print("test_remove_nonexistent_task passed")


if __name__ == "__main__":
    test_add_task()
    test_remove_task()
    test_remove_nonexistent_task()
    print("All tests passed!")