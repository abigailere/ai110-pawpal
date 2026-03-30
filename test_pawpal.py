from pawpal_system import Task, Pet, Owner


# Verifies that a task is correctly added to a pet's task list
# and that the pet's name is automatically assigned to the task
def test_add_task():
    pet = Pet(name="Buddy", species="dog")
    task = Task(title="Walk", duration=30, priority="high")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].title == "Walk"
    assert pet.tasks[0].pet_name == "Buddy"
    print("test_add_task passed")


# Verifies that a task can be removed from a pet's task list by title
def test_remove_task():
    pet = Pet(name="Buddy", species="dog")
    task = Task(title="Walk", duration=30, priority="high")
    pet.add_task(task)

    pet.remove_task("Walk")

    assert len(pet.tasks) == 0
    print("test_remove_task passed")


# Verifies that removing a task that doesn't exist leaves the task list unchanged
def test_remove_nonexistent_task():
    pet = Pet(name="Buddy", species="dog")
    task = Task(title="Walk", duration=30, priority="high")
    pet.add_task(task)

    pet.remove_task("Bath")  # doesn't exist

    assert len(pet.tasks) == 1  # Walk should still be there
    print("test_remove_nonexistent_task passed")


# Verifies that adding the same pet twice does not create a duplicate in the owner's pet list
def test_add_duplicate_pet():
    owner = Owner(name="Alex", time_available=60)
    pet = Pet(name="Buddy", species="dog")

    owner.add_pet(pet)
    owner.add_pet(pet)  # adding the same pet again

    assert len(owner.pets) == 1  # should still only have one
    print("test_add_duplicate_pet passed")


# Verifies that a pet is correctly added to an owner's pet list
def test_add_pet():
    owner = Owner(name="Alex", time_available=60)
    pet = Pet(name="Buddy", species="dog")

    owner.add_pet(pet)

    assert len(owner.pets) == 1
    assert owner.pets[0].name == "Buddy"
    print("test_add_pet passed")


if __name__ == "__main__":
    test_add_task()
    test_remove_task()
    test_remove_nonexistent_task()
    test_add_duplicate_pet()
    test_add_pet()
    print("All tests passed!")