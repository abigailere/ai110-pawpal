# PawPal+ Core Features

---

## Class Design

### Owner
- `name`
- `time_available` (minutes per day)
- `pets` (list of Pet objects)
- `generate_schedule()` — uses time_available and all pet tasks to build a daily plan

### Pet
- `name`
- `species` (dog, cat, other)
- `tasks` (list of Task objects)

### Task
- `title`
- `duration` (minutes)
- `priority` (low / medium / high)
- `is_done` (bool)

**Relationships:**
- Owner has many Pets (one-to-many)
- Pet has many Tasks (one-to-many)

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
