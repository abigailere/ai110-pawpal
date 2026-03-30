import sys
sys.stdout.reconfigure(encoding="utf-8")

from pawpal_system import Task, Pet, Owner, Scheduler

# --- Setup ---
owner = Owner(name="Alex", time_available=90)  # 90 minutes available today

dog = Pet(name="Buddy", species="dog")
cat = Pet(name="Luna", species="cat")
dog2 = Pet(name="Al", species="dog")  # duplicate pet to test edge case

# --- Add Tasks ---
dog.add_task(Task(title="Morning walk",     duration=30, priority="high"))
dog.add_task(Task(title="Feed breakfast",   duration=10, priority="high"))
dog.add_task(Task(title="Bath time",        duration=25, priority="low"))
dog.add_task(Task(title="sleep",        duration=20, priority="low"))

dog2.add_task(Task(title="Morning walk",     duration=30, priority="high"))
dog2.add_task(Task(title="give medicine",   duration=10, priority="high"))

cat.add_task(Task(title="Clean litter box", duration=15, priority="medium"))
cat.add_task(Task(title="Playtime",         duration=20, priority="medium"))

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