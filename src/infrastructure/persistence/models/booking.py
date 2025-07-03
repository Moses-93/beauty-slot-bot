from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean,
    Time,
    Integer,
    Column,
    DateTime,
    ForeignKey,
    Date,
    func,
)

from .base import Base


class TimeSlotModel(Base):
    __tablename__ = "time_slots"
    id = Column(Integer, primary_key=True, index=True)
    master_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    date = Column(Date, nullable=False)
    start_time = Column(Time(True), nullable=False)
    end_time = Column(Time(True), nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    is_booked = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime(True), nullable=False, default=func.now())
    updated_at = Column(
        DateTime(True), nullable=False, default=func.now(), onupdate=func.now()
    )

    booking = relationship("BookingModel", back_populates="time_slot", uselist=False)


class BookingModel(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    client_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    date_id = Column(Integer, ForeignKey("dates.id", ondelete="CASCADE"))
    reminder_time = Column(DateTime(True), nullable=True)
    is_active = Column(Boolean, default=True, index=True)

    created_at = Column(DateTime(True), nullable=False, default=func.now())
    updated_at = Column(
        DateTime(True), nullable=False, default=func.now(), onupdate=func.now()
    )

    time_slot = relationship("TimeSlotModel", back_populates="booking", uselist=False)
    service = relationship("ServiceModel", back_populates="bookings", uselist=False)
