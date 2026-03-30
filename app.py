import streamlit as st
from datetime import date
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Your daily pet care planner.")

# ── Session state vault ──────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = None

# ── Owner Setup ──────────────────────────────────────────────────────────────
with st.expander("👤 Owner Setup", expanded=st.session_state.owner is None):
    col1, col2 = st.columns(2)
    with col1:
        owner_name = st.text_input("Owner name", value="Jordan")
    with col2:
        time_available = st.number_input("Time available (min)", min_value=10, max_value=480, value=90)

    if st.button("Set Owner"):
        st.session_state.owner = Owner(name=owner_name, time_available=time_available)
        st.success(f"Owner set: {owner_name} ({time_available} min available today)")

if st.session_state.owner is None:
    st.info("Set an owner above to get started.")
    st.stop()

owner: Owner = st.session_state.owner
st.markdown(f"**Owner:** {owner.name} &nbsp;|&nbsp; **Time budget:** {owner.time_available} min")

st.divider()

# ── Add Pet ──────────────────────────────────────────────────────────────────
st.subheader("🐶 Pets")
with st.form("add_pet_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])
    submitted = st.form_submit_button("Add Pet")
    if submitted:
        if not pet_name.strip():
            st.warning("Please enter a pet name.")
        else:
            before = len(owner.pets)
            owner.add_pet(Pet(name=pet_name.strip(), species=species))
            if len(owner.pets) > before:
                st.success(f"Added {species} '{pet_name}'.")
            else:
                st.warning(f"'{pet_name}' already exists.")

if owner.pets:
    SPECIES_ICON = {"dog": "🐶", "cat": "🐱", "other": "🐾"}
    cols = st.columns(len(owner.pets))
    for col, pet in zip(cols, owner.pets):
        icon = SPECIES_ICON.get(pet.species, "🐾")
        col.metric(label=f"{icon} {pet.name}", value=pet.species, delta=f"{len(pet.tasks)} task(s)")
else:
    st.info("No pets yet. Add one above.")

st.divider()

# ── Add Task ─────────────────────────────────────────────────────────────────
st.subheader("📋 Tasks")
if not owner.pets:
    st.info("Add a pet first before adding tasks.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col4:
            task_pet = st.selectbox("For pet", [p.name for p in owner.pets])

        col5, col6, col7 = st.columns(3)
        with col5:
            recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"])
        with col6:
            due_date = st.date_input("Due date", value=date.today())
        with col7:
            start_hour = st.number_input("Start hour (0–23)", min_value=0, max_value=23, value=8)

        if st.form_submit_button("Add Task"):
            pet = next(p for p in owner.pets if p.name == task_pet)
            pet.add_task(Task(
                title=task_title,
                duration=int(duration),
                priority=priority,
                recurrence=recurrence if recurrence != "none" else None,
                due_date=due_date,
                start_time=start_hour * 60,
            ))
            st.success(f"Added '{task_title}' to {task_pet}.")

    # Task list with complete buttons
    all_tasks_flat = [(p, t) for p in owner.pets for t in p.tasks]
    if all_tasks_flat:
        scheduler = Scheduler(owner)
        for pet, task in all_tasks_flat:
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            col1.markdown(f"{'~~' if task.is_done else ''}**{task.title}** ({pet.name}){'~~' if task.is_done else ''}")
            col2.caption(f"{task.duration} min")
            col3.caption(task.priority)
            col4.caption(task.recurrence or "—")
            if task.is_done:
                col5.success("Done")
            else:
                if col5.button("✅ Done", key=f"done_{pet.name}_{task.title}"):
                    next_task = scheduler.complete_task(task)
                    if next_task:
                        st.success(f"'{task.title}' done! Next occurrence queued for {next_task.due_date}.")
                    else:
                        st.success(f"'{task.title}' marked complete.")
                    st.rerun()
    else:
        st.info("No tasks yet.")

st.divider()

# ── Schedule ─────────────────────────────────────────────────────────────────
st.subheader("📅 Generate Schedule")

sort_mode = st.radio("Sort tasks by", ["Priority (high → low)", "Duration (short → long)"], horizontal=True)

if st.button("Generate Schedule", type="primary"):
    scheduler = Scheduler(owner)
    all_tasks = scheduler.collect_all_tasks()

    if not all_tasks:
        st.warning("No tasks to schedule. Add some tasks first.")
    else:
        # Sort according to chosen mode
        if sort_mode == "Priority (high → low)":
            sorted_tasks = scheduler.sort_by_priority(all_tasks)
        else:
            sorted_tasks = scheduler.sort_by_time(all_tasks)

        scheduled = scheduler.fit_to_time(sorted_tasks)
        total_time = sum(t.duration for t in scheduled)

        # ── Conflict warnings ────────────────────────────────────────────────
        conflicts = scheduler.detect_conflicts(scheduled)
        if conflicts:
            st.error(f"⚠️ {len(conflicts)} scheduling conflict(s) found — review before your day starts!")
            for warning in conflicts:
                # Parse out the two task names for a friendlier message
                st.warning(warning)
        else:
            st.success("No scheduling conflicts detected.")

        # ── Summary metrics ──────────────────────────────────────────────────
        col1, col2, col3 = st.columns(3)
        col1.metric("Tasks scheduled", len(scheduled))
        col2.metric("Time used", f"{total_time} min")
        col3.metric("Time remaining", f"{owner.time_available - total_time} min")

        # ── Schedule table ───────────────────────────────────────────────────
        if scheduled:
            st.markdown("### Today's Plan")
            schedule_rows = []
            for i, t in enumerate(scheduled, 1):
                start_str = f"{t.start_time // 60:02d}:{t.start_time % 60:02d}" if t.start_time is not None else "—"
                schedule_rows.append({
                    "#": i,
                    "Task": t.title,
                    "Pet": t.pet_name,
                    "Start": start_str,
                    "Duration": f"{t.duration} min",
                    "Priority": t.priority,
                    "Recurs": t.recurrence or "—",
                })
            st.table(schedule_rows)

        # ── Skipped tasks ────────────────────────────────────────────────────
        scheduled_titles = {t.title for t in scheduled}
        skipped = [t for t in all_tasks if t.title not in scheduled_titles]
        if skipped:
            with st.expander(f"⏭️ {len(skipped)} task(s) skipped (not enough time)"):
                for t in skipped:
                    st.markdown(f"- **{t.title}** ({t.pet_name}) — {t.duration} min | {t.priority} priority")

        # ── Explanation ──────────────────────────────────────────────────────
        with st.expander("📝 Full explanation"):
            st.text(scheduler.explain_plan(scheduled, scheduler.sort_by_priority(all_tasks)))