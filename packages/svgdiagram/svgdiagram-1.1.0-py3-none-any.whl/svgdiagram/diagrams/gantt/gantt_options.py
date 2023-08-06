from pydantic import BaseModel, Field
from datetime import date, time
from typing import List


class GanttOptions(BaseModel):
    public_holidays: List[date] = Field(default_factory=list)
    date_default_time: time = time(12, 0)
