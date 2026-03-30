from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date, timedelta

PRIORITY_RANK = {"low": 0, "medium": 1, "high": 2}
RECURRENCE_DAYS = {"daily": 1, "weekly": 7}

@dataclass
class Task:
    title: str
    duration: int                      # minutes
    priority: str                      # "low", "medium", "high"
    is_done: bool = False
    pet_name: str = ""                 # which pet this task belongs to
    recurrence: Optional[str] = None  # "daily", "weekly", or None
    due_date: date = field(default_factory=date.today)
    start_time: Optional[int] = None  # minutes from midnight, e.g. 480 = 8:00 AM

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as done and handle recurrence.

        Sets is_done to True. If the task has a recurrence value ("daily" or
        "weekly"), calculates the next due date using timedelta and returns a
        brand-new Task with the same attributes but a fresh due_date and
        is_done=False. Returns None for one-off tasks so the caller knows no
        follow-up is needed.

        Time complexity: O(1) — only a dict lookup and date addition.
        """
        self.is_done = True
        if self.recurrence in RECURRENCE_DAYS:
            next_due = self.due_date + timedelta(days=RECURRENCE_DAYS[self.recurrence])
            return Task(
                title=self.title,
                duration=self.duration,
                priority=self.priority,
                pet_name=self.pet_name,
                recurrence=self.recurrence,
                due_date=next_due,
            )
        return None

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
        self._pets: dict[str, Pet] = {}  # keyed by pet name for O(1) lookup

    @property
    def pets(self) -> List[Pet]:
        return list(self._pets.values())

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's dict, ignoring duplicates by name — O(1)."""
        if pet.name in self._pets:
            print(f"Pet '{pet.name}' already exists.")
            return
        self._pets[pet.name] = pet


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

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted from shortest to longest duration.

        Uses Python's built-in sorted() with task.duration as the key.
        Shortest tasks appear first, which is useful when the goal is to fit
        as many tasks as possible into a limited time window.

        Time complexity: O(n log n) — Timsort via sorted().
        """
        return sorted(tasks, key=lambda t: t.duration)

    def fit_to_time(self, tasks: List[Task]) -> List[Task]:
        """Return the subset of tasks that fit within the owner's available time.

        Implements a greedy algorithm: walks the task list once in order,
        accumulating total duration. A task is included only if adding it would
        not exceed time_available. Because tasks should be sorted by priority
        before calling this method, the highest-value tasks are always
        considered first.

        Time complexity: O(n) — single pass through the task list.
        """
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

    def detect_conflicts(self, scheduled: List[Task]) -> List[str]:
        """Return warning messages for any two scheduled tasks whose time windows overlap.

        Uses pairwise interval overlap detection: two tasks A and B conflict if
        A.start < B.end AND B.start < A.end. Tasks without a start_time are
        silently skipped so the method never crashes on incomplete data.

        Returns a list of human-readable warning strings (empty if no conflicts).

        Time complexity: O(n²) — every pair of timed tasks is compared once.
        """
        warnings = []
        timed = [t for t in scheduled if t.start_time is not None]
        for i in range(len(timed)):
            for j in range(i + 1, len(timed)):
                a, b = timed[i], timed[j]
                a_start, b_start = a.start_time, b.start_time
                assert a_start is not None and b_start is not None  # guaranteed by timed filter
                a_end = a_start + a.duration
                b_end = b_start + b.duration
                if a_start < b_end and b_start < a_end:
                    warnings.append(
                        f"WARNING: '{a.title}' ({a.pet_name}) and '{b.title}' ({b.pet_name}) overlap — "
                        f"{a_start//60:02d}:{a_start%60:02d}–{a_end//60:02d}:{a_end%60:02d} "
                        f"vs {b_start//60:02d}:{b_start%60:02d}–{b_end//60:02d}:{b_end%60:02d}"
                    )
        return warnings

    def complete_task(self, task: Task) -> Optional[Task]:
        """Mark a task complete. If it recurs, add the next occurrence to the pet's task list."""
        next_task = task.mark_complete()
        if next_task:
            for pet in self.owner.pets:
                if pet.name == task.pet_name:
                    pet.add_task(next_task)
                    break
        return next_task

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