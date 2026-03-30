from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration: int        # minutes
    priority: str        # "low", "medium", "high"
    is_done: bool = False


@dataclass
class Pet:
    name: str
    species: str         # "dog", "cat", "other"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def remove_task(self, title: str):
        pass


class Owner:
    def __init__(self, name: str, time_available: int):
        self.name = name
        self.time_available = time_available  # minutes per day
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def generate_schedule(self) -> List[Task]:
        # Collect all tasks from all pets
        # Sort by priority
        # Fit tasks into time_available
        # Return ordered list of scheduled tasks
        pass