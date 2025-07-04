from pydantic import BaseModel, Field
from typing import Optional
from datetime import timedelta


class ServiceDTO(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str
    price: int
    duration: timedelta
    is_active: bool = Field(default=True)
