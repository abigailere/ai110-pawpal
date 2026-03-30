# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling

PawPal+ goes beyond a basic task list with several intelligent scheduling features:

- **Priority-based scheduling** — tasks are ranked high/medium/low and the highest-priority tasks are always scheduled first within the owner's available time.
- **Duration-based sorting** — tasks can alternatively be sorted shortest-first to maximise the number of tasks that fit in a day.
- **Greedy time fitting** — the scheduler walks the sorted task list once and adds each task only if it fits within the remaining time budget, then stops. No backtracking needed.
- **Conflict detection** — if two tasks have overlapping time windows, the app flags a warning with the exact times so the owner can fix it before the day starts. Back-to-back tasks (one ends where the next begins) are not flagged.
- **Recurring tasks** — tasks can repeat daily or weekly. When marked complete, the next occurrence is automatically created with the correct due date using Python timedelta. One-off tasks simply close out with no follow-up.
- **O(1) pet lookup** — pets are stored in a dictionary keyed by name, so duplicate checks and lookups are instant regardless of how many pets the owner has.

---

## 📸 Demo

<a href="/course_images/ai110/pawpal_demo.png" target="_blank"><img src='/course_images/ai110/pawpal_demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

---

## Testing PawPal+

Run the full test suite with:

```bash
python -m pytest test/test_pawpal.py -v
```

The suite covers 20 tests across these categories:

| Category | What is tested |
|---|---|
| **Core behaviour** | Adding/removing tasks, adding pets, duplicate pet prevention, marking tasks complete |
| **Sorting correctness** | Priority order (high to medium to low), duration order (shortest to longest) |
| **Recurrence logic** | Daily task creates a new task due the next day; weekly task creates one due 7 days later; non-recurring tasks produce no follow-up |
| **Conflict detection** | Same start time is flagged; back-to-back tasks are not flagged; tasks with no start time are safely skipped |
| **Edge cases** | Pet with no tasks, owner with zero time available, single task that exceeds the time budget, tasks that exactly fill the time budget |

### Confidence Level: ★★★★☆ (4/5)

The core scheduling logic — sorting, greedy fitting, recurrence, and conflict detection — is fully tested and all 20 tests pass. One star is held back because the UI layer (app.py) has no automated tests; Streamlit interactions can only be verified manually, so UI bugs would not be caught by the test suite.

---
