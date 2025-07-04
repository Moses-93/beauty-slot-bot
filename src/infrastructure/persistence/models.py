from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    BigInteger,
    Boolean,
    Enum,
    Interval,
    Text,
    Time,
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey,
    Date,
    func,
)
from src.domain.enums.user_role import UserRole

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

    bookings = relationship("BookingModel", back_populates="date")


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

    date = relationship("DateModel", back_populates="bookings", uselist=False)
    service = relationship("ServiceModel", back_populates="bookings", uselist=False)
    user = relationship("UserModel", back_populates="bookings", uselist=False)


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=True, unique=True)
    chat_id = Column(BigInteger, nullable=False, unique=True, index=True)
    role = Column(
        Enum(UserRole, native_enum=False), default=UserRole.CLIENT, nullable=False
    )

    created_at = Column(DateTime(True), nullable=False, default=func.now())
    updated_at = Column(
        DateTime(True), nullable=False, default=func.now(), onupdate=func.now()
    )

    bookings = relationship("BookingModel", back_populates="user")
    contact = relationship("ContactModel", back_populates="user", uselist=False)

    def __str__(self):
        return f"Ім'я: {self.name}"


class ContactModel(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    phone_number = Column(String, nullable=True)
    address = Column(String, nullable=True)
    telegram_link = Column(String, nullable=True)
    instagram_link = Column(String, nullable=True)
    google_maps_link = Column(String, nullable=True)
    about = Column(Text, nullable=True)
    work_start_time = Column(Time(True), nullable=False)
    work_end_time = Column(Time(True), nullable=False)

    created_at = Column(DateTime(True), nullable=False, default=func.now())
    updated_at = Column(
        DateTime(True), nullable=False, default=func.now(), onupdate=func.now()
    )

    user = relationship("UserModel", back_populates="contact")
