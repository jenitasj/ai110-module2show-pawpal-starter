from pawpal_system import Owner, Pet, Task, Scheduler

def test_mark_complete_changes_status():
    task = Task(
        title="Feed breakfast",
        category="feeding",
        duration_minutes=10,
        priority="high",
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog")
    task = Task(
        title="Morning walk",
        category="exercise",
        duration_minutes=20,
        priority="medium",
    )

    assert len(pet.tasks) == 0
    pet.add_task(task)
    assert len(pet.tasks) == 1


def test_sort_by_time_returns_tasks_in_chronological_order():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    task1 = Task(
        title="Evening walk",
        category="exercise",
        duration_minutes=20,
        priority="medium",
        preferred_time="18:00",
    )
    task2 = Task(
        title="Breakfast",
        category="feeding",
        duration_minutes=10,
        priority="high",
        preferred_time="07:30",
    )
    task3 = Task(
        title="Medication",
        category="health",
        duration_minutes=5,
        priority="high",
        preferred_time="09:00",
    )

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time(owner.get_all_tasks())

    assert sorted_tasks[0][1].title == "Breakfast"
    assert sorted_tasks[1][1].title == "Medication"
    assert sorted_tasks[2][1].title == "Evening walk"


def test_mark_task_complete_creates_next_daily_recurring_task():
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
    assert pet.tasks[1].title == "Morning walk"
    assert pet.tasks[1].scheduled_date == "2026-03-30"
    assert pet.tasks[1].completed is False


def test_detect_conflicts_flags_duplicate_times():
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task(
            title="Walk",
            category="exercise",
            duration_minutes=20,
            priority="high",
            preferred_time="08:00",
        )
    )
    cat.add_task(
        Task(
            title="Medication",
            category="health",
            duration_minutes=5,
            priority="medium",
            preferred_time="08:00",
        )
    )

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_filter_tasks_by_status_returns_only_matching_tasks():
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


def test_build_daily_schedule_returns_empty_list_when_no_tasks():
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule()

    assert schedule == []