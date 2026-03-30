from dataclasses import dataclass, field
from typing import List

PRIORITY_RANK = {"low": 0, "medium": 1, "high": 2}

@dataclass
class Task:
    title: str
    duration: int        # minutes
    priority: str        # "low", "medium", "high"
    is_done: bool = False
    pet_name: str = ""   # which pet this task belongs to

    def mark_complete(self):
        """Mark this task as done."""
        self.is_done = True

@dataclass
class Pet:
    name: str
    species: str         # "dog", "cat", "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Assign this pet's name to the task and add it to the task list."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, title: str):
        """Remove the task with the given title from the task list; does nothing if not found."""
        # Rebuilds self.tasks keeping only tasks whose title does not match the given title.
        # Loops through every task t in self.tasks, checks t.title != title:
        #   - True  → task is kept
        #   - False → task is dropped
        self.tasks = [t for t in self.tasks if t.title != title]


class Owner:
    def __init__(self, name: str, time_available: int):
        self.name = name
        self.time_available = time_available  # minutes per day
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list, ignoring duplicates by name."""
        if any(p.name == pet.name for p in self.pets):
            print(f"Pet '{pet.name}' already exists.")
            return
        self.pets.append(pet)


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def collect_all_tasks(self) -> List[Task]:
        """Return a flat list of all tasks across every pet the owner has."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted from highest to lowest priority."""
        return sorted(tasks, key=lambda t: PRIORITY_RANK[t.priority], reverse=True)

    def fit_to_time(self, tasks: List[Task]) -> List[Task]:
        """Return the subset of tasks that fit within the owner's available time."""
        scheduled = []
        total = 0
        for task in tasks:
            if total + task.duration <= self.owner.time_available:
                scheduled.append(task)
                total += task.duration
        return scheduled

    def generate_schedule(self) -> List[Task]:
        """Collect, sort by priority, and fit tasks into the owner's available time."""
        all_tasks = self.collect_all_tasks()
        sorted_tasks = self.sort_by_priority(all_tasks)
        return self.fit_to_time(sorted_tasks)

    def explain_plan(self, scheduled: List[Task], all_tasks: List[Task]) -> str:
        """Return a string explaining why each task was included or skipped."""
        lines = []
        scheduled_titles = {t.title for t in scheduled}
        for task in all_tasks:
            if task.title in scheduled_titles:
                lines.append(f"✓ '{task.title}' ({task.pet_name}) included — priority: {task.priority}, duration: {task.duration} min")
            else:
                lines.append(f"✗ '{task.title}' ({task.pet_name}) skipped — not enough time remaining")
        return "\n".join(lines)