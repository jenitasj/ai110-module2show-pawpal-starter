from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(title, schedule):
    print(f"\n=== {title} ===")
    if not schedule:
        print("No tasks found.")
        return

    for index, (pet, task) in enumerate(schedule, start=1):
        time_text = task.preferred_time if task.preferred_time else "No set time"
        date_text = task.scheduled_date if task.scheduled_date else "No set date"
        print(
            f"{index}. {date_text} | {time_text} | {pet.name} ({pet.species}) | "
            f"{task.title} | {task.priority.title()} priority | "
            f"{task.duration_minutes} min | Completed: {task.completed}"
        )


def print_task_list(title, tasks):
    print(f"\n=== {title} ===")
    if not tasks:
        print("No tasks found.")
        return

    for index, task in enumerate(tasks, start=1):
        time_text = task.preferred_time if task.preferred_time else "No set time"
        date_text = task.scheduled_date if task.scheduled_date else "No set date"
        print(
            f"{index}. {date_text} | {time_text} | {task.title} | "
            f"{task.priority.title()} priority | Completed: {task.completed}"
        )


def print_messages(title, messages):
    print(f"\n=== {title} ===")
    if not messages:
        print("None")
        return

    for message in messages:
        print(f"- {message}")


def main():
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog", age=3)
    cat = Pet(name="Luna", species="cat", age=5)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            title="Morning walk",
            category="exercise",
            duration_minutes=20,
            priority="high",
            preferred_time="08:00",
            scheduled_date="2026-03-29",
            recurring=True,
            recurrence_pattern="daily",
        )
    )

    dog.add_task(
        Task(
            title="Breakfast feeding",
            category="feeding",
            duration_minutes=10,
            priority="high",
            preferred_time="07:30",
            scheduled_date="2026-03-29",
        )
    )

    cat.add_task(
        Task(
            title="Medication",
            category="health",
            duration_minutes=5,
            priority="medium",
            preferred_time="08:00",
            scheduled_date="2026-03-29",
            recurring=True,
            recurrence_pattern="daily",
        )
    )

    cat.add_task(
        Task(
            title="Vet appointment prep",
            category="appointment",
            duration_minutes=15,
            priority="low",
            preferred_time="18:00",
            scheduled_date="2026-03-29",
        )
    )

    scheduler = Scheduler(owner)

    daily_schedule = scheduler.build_daily_schedule()
    print_schedule("Daily Schedule (Priority + Time)", daily_schedule)

    time_sorted = scheduler.sort_by_time(owner.get_all_tasks())
    print_schedule("Tasks Sorted by Time", time_sorted)

    incomplete_tasks = scheduler.filter_tasks_by_status(False)
    print_schedule("Incomplete Tasks", incomplete_tasks)

    luna_tasks = scheduler.filter_tasks_by_pet("Luna")
    print_task_list("Tasks for Luna", luna_tasks)

    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())
    print_messages("Conflict Warnings", conflicts)

    scheduler.mark_task_complete("Mochi", "Morning walk")
    updated_mochi_tasks = scheduler.filter_tasks_by_pet("Mochi")
    print_task_list("Mochi Tasks After Completing Recurring Walk", updated_mochi_tasks)

    completed_tasks = scheduler.filter_tasks_by_status(True)
    print_schedule("Completed Tasks", completed_tasks)


if __name__ == "__main__":
    main()