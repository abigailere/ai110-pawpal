# PawPal+ Core Features

---

## Class Design

### Owner
- `name`
- `time_available` (minutes per day)
- `pets` (list of Pet objects)

### Pet
- `name`
- `species` (dog, cat, other)
- `tasks` (list of Task objects)
- `add_task()`, `remove_task()`

### Task
- `title`
- `duration` (minutes)
- `priority` (low / medium / high)
- `is_done` (bool)

### Scheduler (the "Brain")
- `owner` (the Owner it manages)
- `collect_all_tasks()` — gathers tasks across all pets
- `sort_by_priority()` — ranks tasks high → low
- `fit_to_time()` — drops tasks that exceed time_available
- `generate_schedule()` — returns the final ordered plan
- `explain_plan()` — describes why each task was included or skipped

**Relationships:**
- Owner has many Pets (one-to-many)
- Pet has many Tasks (one-to-many)
- Scheduler manages one Owner and operates on its Tasks

---

## App Features

### 1. Owner & Pet Profiles
- Enter owner name and available time for the day
- Add one or more pets with name and species

### 2. Task Management
- Add/edit/delete care tasks per pet (walks, feeding, meds, grooming, enrichment)
- Each task requires: title, duration, priority
- Optional: preferred time of day, frequency (daily vs. one-time)

### 3. Scheduling Engine
- Produces an ordered daily plan from available time + task list
- High-priority tasks always make the cut
- Drops lower-priority tasks when time runs out
- Core question: given `time_available` and all tasks across all pets, which tasks get included and in what order?

### 4. Plan Display & Explanation
- Shows the schedule as a clear timeline or table
- Explains why each task was included or skipped
- Example: "Skipped afternoon enrichment because you only had 90 min and medication and feeding were higher priority"

### 5. Tests
- Scheduler picks high-priority tasks first
- Scheduler respects time limits
- Scheduler handles an empty task list

---

## Nice-to-Haves
- Save/load task list between sessions (session_state or JSON file)
- Recurring vs. one-time tasks

---

## Reminders

- **`Task` needs a `pet_name` field** — once tasks are flattened in `collect_all_tasks`, pet context is lost. `explain_plan` can't say which pet's task was skipped without it.
- **`Owner.add_pet` must actually append to `self.pets`** — `Scheduler` depends on `owner.pets` being populated; if it's a stub, `collect_all_tasks` will always return nothing.
- **`sort_by_priority` needs an explicit rank map** — sorting `"low"`, `"medium"`, `"high"` as strings gives the wrong order (`high < low < medium` lexicographically). Use `{"low": 0, "medium": 1, "high": 2}`.
- **`fit_to_time` needs a tie-breaking rule** — if two tasks have equal priority and only one fits, define which wins (e.g., shorter duration takes precedence).
- **`explain_plan` is disconnected from `generate_schedule`** — `explain_plan` needs the pre-fit `all_tasks` list, but `generate_schedule` doesn't capture or pass it. Save `all_tasks` before fitting and thread it through.
- **Build `Owner` fully before instantiating `Scheduler`** — `Scheduler` takes a snapshot of `owner` at init time; pets added after won't be visible unless the reference is live.
