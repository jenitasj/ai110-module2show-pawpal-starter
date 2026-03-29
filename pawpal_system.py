from dataclasses import dataclass, field
from typing import List, Optional


PRIORITY_RANK = {
    "high": 3,
    "medium": 2,
    "low": 1,
}


@dataclass
class Task:
    title: str
    category: str
    duration_minutes: int
    priority: str
    preferred_time: Optional[str] = None
    scheduled_date: Optional[str] = None
    recurring: bool = False
    recurrence_pattern: Optional[str] = None
    completed: bool = False

    def describe(self) -> str:
        """Return a readable description of the task."""
        time_text = self.preferred_time if self.preferred_time else "unspecified time"
        status = "completed" if self.completed else "not completed"
        return (
            f"{self.title} ({self.category}) - {self.duration_minutes} min, "
            f"priority: {self.priority}, time: {time_text}, status: {status}"
        )

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    preferences: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove a task by title."""
        self.tasks = [task for task in self.tasks if task.title != task_title]

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    name: str
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's profile."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> List[tuple[Pet, Task]]:
        """Return all tasks across all pets, paired with their pet."""
        all_tasks = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    def __init__(self, owner: Owner):
        """Initialize the scheduler for one owner."""
        self.owner = owner

    def build_daily_schedule(self) -> List[tuple[Pet, Task]]:
        """Build a daily schedule using unfinished tasks sorted by priority and time."""
        tasks = self.owner.get_all_tasks()
        tasks = [(pet, task) for pet, task in tasks if not task.completed]
        return self.sort_tasks(tasks)

    def sort_tasks(self, tasks: List[tuple[Pet, Task]]) -> List[tuple[Pet, Task]]:
        """Sort tasks by priority first, then preferred time."""
        def sort_key(item: tuple[Pet, Task]):
            pet, task = item
            priority_value = PRIORITY_RANK.get(task.priority.lower(), 0)
            time_value = task.preferred_time if task.preferred_time is not None else "99:99"
            return (-priority_value, time_value, pet.name.lower(), task.title.lower())

        return sorted(tasks, key=sort_key)

    def detect_conflicts(self, tasks: List[tuple[Pet, Task]]) -> List[str]:
        """Return messages for tasks that share the same preferred time."""
        seen_times = {}
        conflicts = []

        for pet, task in tasks:
            if task.preferred_time is None:
                continue

            if task.preferred_time in seen_times:
                other_pet, other_task = seen_times[task.preferred_time]
                conflicts.append(
                    f"Conflict at {task.preferred_time}: "
                    f"{other_pet.name} - {other_task.title} and {pet.name} - {task.title}"
                )
            else:
                seen_times[task.preferred_time] = (pet, task)

        return conflicts

    def explain_schedule(self, schedule: List[tuple[Pet, Task]]) -> List[str]:
        """Explain why each task appears in the schedule."""
        explanations = []

        for pet, task in schedule:
            time_text = task.preferred_time if task.preferred_time else "no preferred time"
            explanations.append(
                f"{pet.name}: '{task.title}' was scheduled because it is "
                f"{task.priority} priority and preferred for {time_text}."
            )

        return explanations