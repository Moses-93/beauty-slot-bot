from pydantic import BaseModel, Field
from datetime import date as Date, time


class DateDTO(BaseModel):
    date: Date
    deactivation_time: time
    is_active: bool = Field(default=True)
