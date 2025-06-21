from pydantic import BaseModel, Field
from typing import Optional
from datetime import date as Date, time


class DateDTO(BaseModel):
    id: Optional[int] = Field(default=None)
    date: Date
    deactivation_time: time
    is_active: bool = Field(default=True)
