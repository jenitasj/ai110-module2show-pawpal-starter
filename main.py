from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(schedule):
    print("\n=== Today's Schedule ===")
    if not schedule:
        print("No tasks scheduled for today.")
        return

    for index, (pet, task) in enumerate(schedule, start=1):
        time_text = task.preferred_time if task.preferred_time else "No set time"
        print(
            f"{index}. {time_text} | {pet.name} ({pet.species}) | "
            f"{task.title} | {task.priority.title()} priority | "
            f"{task.duration_minutes} min"
        )


def print_explanations(explanations):
    print("\n=== Schedule Explanations ===")
    if not explanations:
        print("No explanations available.")
        return

    for explanation in explanations:
        print(f"- {explanation}")


def main():
    owner = Owner(name="Jordan", preferences=["morning walks", "evening feeding"])

    dog = Pet(name="Mochi", species="dog", age=3, preferences=["short walks"])
    cat = Pet(name="Luna", species="cat", age=5, preferences=["quiet evenings"])

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            title="Morning walk",
            category="exercise",
            duration_minutes=20,
            priority="high",
            preferred_time="08:00",
        )
    )

    dog.add_task(
        Task(
            title="Breakfast feeding",
            category="feeding",
            duration_minutes=10,
            priority="high",
            preferred_time="07:30",
        )
    )

    cat.add_task(
        Task(
            title="Medication",
            category="health",
            duration_minutes=5,
            priority="medium",
            preferred_time="09:00",
        )
    )

    cat.add_task(
        Task(
            title="Vet appointment prep",
            category="appointment",
            duration_minutes=15,
            priority="low",
            preferred_time="18:00",
        )
    )

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule()
    explanations = scheduler.explain_schedule(schedule)
    conflicts = scheduler.detect_conflicts(schedule)

    print_schedule(schedule)
    print_explanations(explanations)

    print("\n=== Conflicts ===")
    if conflicts:
        for conflict in conflicts:
            print(f"- {conflict}")
    else:
        print("No conflicts found.")


if __name__ == "__main__":
    main()