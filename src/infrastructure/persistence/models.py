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
    func,
)

Base = declarative_base()


class DateModel(Base):
    __tablename__ = "dates"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    deactivation_time = Column(DateTime(True), nullable=False)
    is_active = Column(Boolean, default=True, index=True)

    created_at = Column(DateTime(True), nullable=False, default=func.now())
    updated_at = Column(
        DateTime(True), nullable=False, default=func.now(), onupdate=func.now()
    )

    bookings = relationship("Booking", back_populates="date")


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
    bookings = relationship("Booking", back_populates="service")


class BookingModel(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    date_id = Column(Integer, ForeignKey("dates.id", ondelete="CASCADE"))
    time = Column(Time(True), nullable=False)
    reminder_time = Column(DateTime(True), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(True), nullable=False, default=func.now())
    updated_at = Column(
        DateTime(True), nullable=False, default=func.now(), onupdate=func.now()
    )

    date = relationship("Date", back_populates="bookings", uselist=False)
    service = relationship("Service", back_populates="bookings", uselist=False)
    user = relationship("User", back_populates="bookings", uselist=False)


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True, unique=True)
    chat_id = Column(String, nullable=False, unique=True, index=True)
    role = Column(String, default="client", nullable=False)

    created_at = Column(DateTime(True), nullable=False, default=func.now())
    updated_at = Column(
        DateTime(True), nullable=False, default=func.now(), onupdate=func.now()
    )

    bookings = relationship("Booking", back_populates="user")

    def __str__(self):
        return f"Ім'я: {self.name}"
