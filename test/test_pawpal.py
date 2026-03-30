from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


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


# Verifies that calling mark_complete() sets the task's is_done status to True
def test_mark_complete():
    task = Task(title="Walk", duration=30, priority="high")

    task.mark_complete()

    assert task.is_done == True
    print("test_mark_complete passed")


# Verifies that adding a task to a pet increases the pet's task count by one
def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="dog")
    count_before = len(pet.tasks)

    pet.add_task(Task(title="Feed", duration=10, priority="high"))

    assert len(pet.tasks) == count_before + 1
    print("test_add_task_increases_count passed")


# ── Happy paths ───────────────────────────────────────────────────────────────

# Verifies that generate_schedule returns all tasks when they fit within time
def test_schedule_happy_path():
    owner = Owner(name="Alex", time_available=60)
    pet = Pet(name="Buddy", species="dog")
    pet.add_task(Task(title="Walk", duration=20, priority="high"))
    pet.add_task(Task(title="Feed", duration=10, priority="medium"))
    owner.add_pet(pet)

    scheduled = Scheduler(owner).generate_schedule()

    assert len(scheduled) == 2
    print("test_schedule_happy_path passed")


# Verifies that sort_by_priority orders high before medium before low
def test_sort_by_priority_order():
    owner = Owner(name="Alex", time_available=120)
    tasks = [
        Task(title="Bath",  duration=10, priority="low"),
        Task(title="Feed",  duration=10, priority="medium"),
        Task(title="Walk",  duration=10, priority="high"),
    ]
    result = Scheduler(owner).sort_by_priority(tasks)

    assert result[0].priority == "high"
    assert result[1].priority == "medium"
    assert result[2].priority == "low"
    print("test_sort_by_priority_order passed")


# Verifies that sort_by_time orders shortest duration first
def test_sort_by_time_order():
    owner = Owner(name="Alex", time_available=120)
    tasks = [
        Task(title="Long",   duration=60, priority="low"),
        Task(title="Short",  duration=10, priority="low"),
        Task(title="Medium", duration=30, priority="low"),
    ]
    result = Scheduler(owner).sort_by_time(tasks)

    assert result[0].title == "Short"
    assert result[2].title == "Long"
    print("test_sort_by_time_order passed")


# Verifies that a daily recurring task queues the next occurrence one day later
def test_daily_recurrence():
    today = date.today()
    task = Task(title="Walk", duration=20, priority="high",
                recurrence="daily", due_date=today)

    next_task = task.mark_complete()

    assert task.is_done is True
    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.is_done is False
    print("test_daily_recurrence passed")


# Verifies that a weekly recurring task queues the next occurrence 7 days later
def test_weekly_recurrence():
    today = date.today()
    task = Task(title="Bath", duration=25, priority="medium",
                recurrence="weekly", due_date=today)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=7)
    print("test_weekly_recurrence passed")


# Verifies tasks that exactly fill time_available are all scheduled
def test_tasks_exactly_fill_time():
    owner = Owner(name="Alex", time_available=30)
    pet = Pet(name="Buddy", species="dog")
    pet.add_task(Task(title="Walk", duration=20, priority="high"))
    pet.add_task(Task(title="Feed", duration=10, priority="medium"))
    owner.add_pet(pet)

    scheduled = Scheduler(owner).generate_schedule()

    assert sum(t.duration for t in scheduled) == 30
    print("test_tasks_exactly_fill_time passed")


# ── Edge cases ────────────────────────────────────────────────────────────────

# Verifies that a pet with no tasks produces an empty schedule without crashing
def test_pet_with_no_tasks():
    owner = Owner(name="Alex", time_available=60)
    owner.add_pet(Pet(name="Buddy", species="dog"))

    scheduled = Scheduler(owner).generate_schedule()

    assert scheduled == []
    print("test_pet_with_no_tasks passed")


# Verifies that no tasks are scheduled when owner has zero time available
def test_owner_zero_time():
    owner = Owner(name="Alex", time_available=0)
    pet = Pet(name="Buddy", species="dog")
    pet.add_task(Task(title="Walk", duration=30, priority="high"))
    owner.add_pet(pet)

    scheduled = Scheduler(owner).generate_schedule()

    assert scheduled == []
    print("test_owner_zero_time passed")


# Verifies that a single task longer than time_available is not scheduled
def test_single_task_exceeds_time():
    owner = Owner(name="Alex", time_available=20)
    pet = Pet(name="Buddy", species="dog")
    pet.add_task(Task(title="Long bath", duration=60, priority="high"))
    owner.add_pet(pet)

    scheduled = Scheduler(owner).generate_schedule()

    assert scheduled == []
    print("test_single_task_exceeds_time passed")


# Verifies that back-to-back tasks (A ends where B starts) are NOT flagged as conflicts
def test_back_to_back_no_conflict():
    owner = Owner(name="Alex", time_available=120)
    pet = Pet(name="Buddy", species="dog")
    pet.add_task(Task(title="Walk", duration=30, priority="high", start_time=480))  # 08:00–08:30
    pet.add_task(Task(title="Feed", duration=30, priority="high", start_time=510))  # 08:30–09:00
    owner.add_pet(pet)

    scheduled = Scheduler(owner).generate_schedule()
    conflicts = Scheduler(owner).detect_conflicts(scheduled)

    assert conflicts == []
    print("test_back_to_back_no_conflict passed")


# Verifies that two tasks at the exact same start time are flagged as a conflict
def test_exact_same_start_time_conflict():
    owner = Owner(name="Alex", time_available=120)
    pet = Pet(name="Buddy", species="dog")
    pet.add_task(Task(title="Walk", duration=30, priority="high", start_time=480))
    pet.add_task(Task(title="Feed", duration=20, priority="medium", start_time=480))
    owner.add_pet(pet)

    scheduled = Scheduler(owner).generate_schedule()
    conflicts = Scheduler(owner).detect_conflicts(scheduled)

    assert len(conflicts) == 1
    print("test_exact_same_start_time_conflict passed")


# Verifies that tasks without a start_time are skipped by detect_conflicts
def test_no_start_time_skipped():
    owner = Owner(name="Alex", time_available=120)
    pet = Pet(name="Buddy", species="dog")
    pet.add_task(Task(title="Walk", duration=30, priority="high"))   # no start_time
    pet.add_task(Task(title="Feed", duration=20, priority="medium")) # no start_time
    owner.add_pet(pet)

    scheduled = Scheduler(owner).generate_schedule()
    conflicts = Scheduler(owner).detect_conflicts(scheduled)

    assert conflicts == []
    print("test_no_start_time_skipped passed")


# Verifies that a non-recurring task marked done returns None and queues nothing
def test_non_recurring_mark_complete():
    owner = Owner(name="Alex", time_available=60)
    pet = Pet(name="Buddy", species="dog")
    task = Task(title="Walk", duration=30, priority="high")
    pet.add_task(task)
    owner.add_pet(pet)

    next_task = Scheduler(owner).complete_task(task)

    assert next_task is None
    assert len(pet.tasks) == 1  # no new task added
    print("test_non_recurring_mark_complete passed")


if __name__ == "__main__":
    test_add_task()
    test_remove_task()
    test_remove_nonexistent_task()
    test_add_duplicate_pet()
    test_add_pet()
    test_mark_complete()
    test_add_task_increases_count()
    # happy paths
    test_schedule_happy_path()
    test_sort_by_priority_order()
    test_sort_by_time_order()
    test_daily_recurrence()
    test_weekly_recurrence()
    test_tasks_exactly_fill_time()
    # edge cases
    test_pet_with_no_tasks()
    test_owner_zero_time()
    test_single_task_exceeds_time()
    test_back_to_back_no_conflict()
    test_exact_same_start_time_conflict()
    test_no_start_time_skipped()
    test_non_recurring_mark_complete()
    print("All tests passed!")