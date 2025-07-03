from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean,
    Interval,
    Integer,
    Column,
    String,
    DateTime,
    func,
)

from .base import Base


class ServiceModel(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    duration = Column(Interval, nullable=False)
    is_active = Column(Boolean, default=True, index=True)

    created_at = Column(DateTime(True), nullable=False, default=func.now())
    updated_at = Column(
        DateTime(True), nullable=False, default=func.now(), onupdate=func.now()
    )

    bookings = relationship("BookingModel", back_populates="service")
