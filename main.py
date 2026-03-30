import sys
sys.stdout.reconfigure(encoding="utf-8")

from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Alex", time_available=180)  # 180 minutes available today

dog = Pet(name="Buddy", species="dog")
cat = Pet(name="Luna", species="cat")
dog2 = Pet(name="Al", species="dog")  # duplicate pet to test edge case

# --- Add Tasks ---
# Morning walk starts at 8:00 AM (480 min) and runs 30 min → ends 8:30
dog.add_task(Task(title="Morning walk",   duration=30, priority="high",   start_time=480))
dog.add_task(Task(title="Feed breakfast", duration=10, priority="high",   start_time=540))
dog.add_task(Task(title="Bath time",      duration=25, priority="low"))
dog.add_task(Task(title="sleep",          duration=20, priority="low"))

dog2.add_task(Task(title="Morning walk",  duration=30, priority="high"))
dog2.add_task(Task(title="give medicine", duration=10, priority="high"))

# Playtime starts at 8:15 AM (495 min) — overlaps with dog's Morning walk (480–510)
cat.add_task(Task(title="Clean litter box", duration=15, priority="medium"))
cat.add_task(Task(title="Playtime",         duration=20, priority="medium", start_time=495))

# --- Register Pets with Owner ---
owner.add_pet(dog)
owner.add_pet(cat)
owner.add_pet(dog2)  

# --- Generate Schedule ---
scheduler  = Scheduler(owner)
all_tasks  = scheduler.collect_all_tasks()
scheduled  = scheduler.generate_schedule()

# --- Print Today's Schedule ---
print("=" * 40)
print(f"   Today's Schedule for {owner.name}")
print("=" * 40)

total_time = 0
for i, task in enumerate(scheduled, start=1):
    status = "[done]" if task.is_done else "[ ]"
    print(f"{i}. {status} {task.title} ({task.pet_name}) — {task.duration} min | priority: {task.priority}")
    total_time += task.duration

print("-" * 40)
print(f"Total time: {total_time} / {owner.time_available} min")
print()
print("--- Schedule Explanation ---")
print(scheduler.explain_plan(scheduled, all_tasks))

print()
print("--- Conflict Detection ---")
conflicts = scheduler.detect_conflicts(scheduled)
if conflicts:
    for warning in conflicts:
        print(warning)
else:
    print("No conflicts detected.")