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

@dataclass
class Pet:
    name: str
    species: str         # "dog", "cat", "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, title: str):
        self.tasks = [t for t in self.tasks if t.title != title]


class Owner:
    def __init__(self, name: str, time_available: int):
        self.name = name
        self.time_available = time_available  # minutes per day
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def collect_all_tasks(self) -> List[Task]:
        # Gather tasks from every pet the owner has
        return []

    def sort_by_priority(self, tasks: List[Task]) -> List[Task]:
        # Return tasks sorted high -> medium -> low
        return []

    def fit_to_time(self, tasks: List[Task]) -> List[Task]:
        # Drop tasks that push total duration over owner's time_available
        return []

    def generate_schedule(self) -> List[Task]:
        # Collect -> sort -> fit -> return final plan
        return []

    def explain_plan(self, scheduled: List[Task], all_tasks: List[Task]) -> str:
        # Describe why each task was included or skipped
        return ""