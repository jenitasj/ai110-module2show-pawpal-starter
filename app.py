import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

if "current_pet" not in st.session_state:
    st.session_state.current_pet = None

st.title("PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save Owner and Pet"):
    st.session_state.owner = Owner(name=owner_name)
    pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(pet)
    st.session_state.current_pet = pet
    st.success(f"Saved owner {owner_name} and pet {pet_name}.")

st.markdown("### Tasks")
st.caption("Add a few tasks. These now feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if st.session_state.current_pet is None:
        st.error("Please save an owner and pet first.")
    else:
        new_task = Task(
            title=task_title,
            category="general",
            duration_minutes=int(duration),
            priority=priority,
            preferred_time=None,
        )
        st.session_state.current_pet.add_task(new_task)
        st.success(f"Added task '{task_title}' for {st.session_state.current_pet.name}.")

if st.session_state.current_pet is not None and st.session_state.current_pet.tasks:
    st.write("Current tasks:")
    task_rows = []
    for task in st.session_state.current_pet.tasks:
        task_rows.append(
            {
                "title": task.title,
                "category": task.category,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "completed": task.completed,
            }
        )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button now calls your scheduling logic.")

if st.button("Generate schedule"):
    if st.session_state.owner is None or not st.session_state.owner.pets:
        st.error("Please save an owner and pet first.")
    else:
        scheduler = Scheduler(st.session_state.owner)
        schedule = scheduler.build_daily_schedule()
        explanations = scheduler.explain_schedule(schedule)
        conflicts = scheduler.detect_conflicts(schedule)

        if schedule:
            st.success("Schedule generated.")

            schedule_rows = []
            for pet, task in schedule:
                schedule_rows.append(
                    {
                        "pet": pet.name,
                        "species": pet.species,
                        "task": task.title,
                        "priority": task.priority,
                        "duration_minutes": task.duration_minutes,
                        "preferred_time": task.preferred_time or "No set time",
                    }
                )

            st.write("### Today's Schedule")
            st.table(schedule_rows)

            st.write("### Explanations")
            for explanation in explanations:
                st.write(f"- {explanation}")

            st.write("### Conflicts")
            if conflicts:
                for conflict in conflicts:
                    st.write(f"- {conflict}")
            else:
                st.write("No conflicts found.")
        else:
            st.info("No tasks available to schedule.")