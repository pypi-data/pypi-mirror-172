from pydantic import BaseModel, Field, Extra
from .task import Task
from .milestone import Milestone
from typing import List


class Swimlane(BaseModel, extra=Extra.forbid):
    name: str
    tasks: List[Task] = Field(default_factory=list)
    milestones: List[Milestone] = Field(default_factory=list)


class CalendarSwimlane(BaseModel, extra=Extra.forbid):
    show_years: bool = False
    show_months: bool = False
    show_weeks: bool = False
    show_days: bool = False

    @classmethod
    def show_all(cls):
        return CalendarSwimlane(
            show_days=True,
            show_months=True,
            show_weeks=True,
            show_years=True,
        )
