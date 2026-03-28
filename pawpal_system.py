from dataclasses import dataclass, field
from typing import List, Optional


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
        """Return a human-readable description of the task."""
        pass

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    preferences: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task for this pet."""
        pass

    def remove_task(self, task_title: str) -> None:
        """Remove a task by title."""
        pass

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        pass


@dataclass
class Owner:
    name: str
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's profile."""
        pass

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        pass

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def build_daily_schedule(self) -> List[Task]:
        """Build a schedule for the owner's pets."""
        pass

    def sort_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority, preferred time, or other scheduling rules."""
        pass

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return a list of scheduling conflicts."""
        pass

    def explain_schedule(self, schedule: List[Task]) -> List[str]:
        """Explain why each task appears in the schedule."""
        pass