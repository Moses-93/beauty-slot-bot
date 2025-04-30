from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
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

Base = declarative_base()


class Date(Base):
    __tablename__ = "dates"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, index=True)
    deactivation_time = Column(DateTime, nullable=False)

    bookings = relationship("Booking", back_populates="date")

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    duration = Column(Interval, nullable=False)

    bookings = relationship("Booking", back_populates="service")

    def __str__(self):
        return f"{self.name}: - {self.price} грн."


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    active = Column(Boolean, default=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String)
    time = Column(Time, nullable=False)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    date_id = Column(Integer, ForeignKey("dates.id", ondelete="CASCADE"))
    reminder_time = Column(Integer, nullable=True)
    created_at = Column(DateTime)

    date = relationship("Date", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")

    def __str__(self):
        return f"Ім'я: {self.name} | Час: {self.time} | Створено в: {self.created_at}"


class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False, unique=True)

    def __str__(self):
        return f"Ім'я: {self.name} | Чат ID: {self.chat_id}"
