from pawpal_system import Owner, Pet, Task, Scheduler


def test_filter_tasks_by_status_returns_only_completed_or_incomplete():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task1 = Task(
        title="Walk",
        category="exercise",
        duration_minutes=20,
        priority="high",
    )
    task2 = Task(
        title="Feed",
        category="feeding",
        duration_minutes=10,
        priority="medium",
    )

    pet.add_task(task1)
    pet.add_task(task2)
    task1.mark_complete()

    scheduler = Scheduler(owner)

    completed = scheduler.filter_tasks_by_status(True)
    incomplete = scheduler.filter_tasks_by_status(False)

    assert len(completed) == 1
    assert completed[0][1].title == "Walk"
    assert len(incomplete) == 1
    assert incomplete[0][1].title == "Feed"


def test_filter_tasks_by_pet_returns_only_that_pets_tasks():
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Walk", "exercise", 20, "high"))
    cat.add_task(Task("Medication", "health", 5, "medium"))

    scheduler = Scheduler(owner)
    luna_tasks = scheduler.filter_tasks_by_pet("Luna")

    assert len(luna_tasks) == 1
    assert luna_tasks[0].title == "Medication"


def test_detect_conflicts_returns_warning_for_same_time():
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Walk", "exercise", 20, "high", preferred_time="08:00"))
    cat.add_task(Task("Medication", "health", 5, "medium", preferred_time="08:00"))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_mark_task_complete_creates_next_recurring_task():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    recurring_task = Task(
        title="Morning walk",
        category="exercise",
        duration_minutes=20,
        priority="high",
        preferred_time="08:00",
        scheduled_date="2026-03-29",
        recurring=True,
        recurrence_pattern="daily",
    )
    pet.add_task(recurring_task)

    scheduler = Scheduler(owner)
    result = scheduler.mark_task_complete("Mochi", "Morning walk")

    assert result is True
    assert pet.tasks[0].completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].scheduled_date == "2026-03-30"
    assert pet.tasks[1].completed is False