from .config import Base
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Boolean,
    Interval,
    Time,
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey,
    Date,
)


class FreeDate(Base):
    __tablename__ = "main_freedate"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    free = Column(Boolean, default=True)
    now = Column(DateTime)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d %H:%M:%S")


class Service(Base):
    __tablename__ = "main_service"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Integer)
    durations = Column(Interval)

    def __str__(self):
        return f"{self.name}: - {self.price} грн."


class Notes(Base):
    __tablename__ = "main_notes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    name = Column(String)
    username = Column(String)
    time = Column(Time, nullable=True)
    reminder_hours = Column(Integer, nullable=True)
    created_at = Column(DateTime)
    service_id = Column(Integer, ForeignKey("main_service.id", ondelete="CASCADE"))
    date_id = Column(Integer, ForeignKey("main_freedate.id", ondelete="CASCADE"))
    free_date = relationship("FreeDate")
    service = relationship("Service")

    def __str__(self):
        return f"Послуга: {self.service.name} | Дата: {self.free_date.date} | Час: {self.time}"
