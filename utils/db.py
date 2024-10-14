from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from os import getenv
from sqlalchemy import (
    Boolean,
    Interval,
    create_engine,
    Integer,
    Column,
    String,
    DateTime,
    ForeignKey,
    Date,
)
from datetime import datetime


URI = getenv("URI")
engine = create_engine(URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class FreeDate(Base):
    __tablename__ = "main_freedate"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    free = Column(Boolean)
    now = Column(DateTime)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d %H:%M:%S")


class Service(Base):
    __tablename__ = "main_service"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(String)
    durations = Column(Interval)  # або можна використовувати Interval

    def __str__(self):
        return f"{self.name} - {self.price} - грн."


class Notes(Base):
    __tablename__ = "main_notes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    time = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    service_id = Column(Integer, ForeignKey("main_service.id"))
    date_id = Column(Integer, ForeignKey("main_freedate.id"))
    free_date = relationship("FreeDate")

    def __str__(self):
        return f"{self.name} - {self.time} - {self.created_at}"


Base.metadata.create_all(bind=engine)

free_dates = (
    session.query(FreeDate)
    .filter(FreeDate.free == True, FreeDate.now > datetime.now())
    .all()
)
services = session.query(Service).all()


def get_service(service_id):
    return session.query(Service).get(service_id)


def get_free_date(date_id):
    return session.query(FreeDate).get(date_id)


def get_notes(id):
    return session.query(Notes).filter_by(date_id=id).all()
