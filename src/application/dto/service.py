from pydantic import BaseModel, Field
from datetime import timedelta


class ServiceDTO(BaseModel):
    title: str
    price: int
    duration: timedelta
    is_active: bool = Field(default=True)
