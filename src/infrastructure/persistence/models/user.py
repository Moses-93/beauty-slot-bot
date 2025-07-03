from sqlalchemy.orm import relationship
from sqlalchemy import (
    BigInteger,
    Enum,
    Text,
    Time,
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey,
    func,
)
from src.domain.enums.user_role import UserRole

from .base import Base


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

    contact = relationship("ContactModel", back_populates="user", uselist=False)

    def __str__(self):
        return f"Ім'я: {self.name}"


class ContactModel(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    master_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
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
