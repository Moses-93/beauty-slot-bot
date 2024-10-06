from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Boolean, create_engine, Integer, Column, String
from os import getenv

URI = getenv('URI')

Base = declarative_base()

engine = create_engine(
    URI
)
Session = sessionmaker(bind=engine)
session = Session()


class FreeDate(Base):
    __tablename__ = "main_freedate"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    free = Column(Boolean)

    def __str__(self):
        return self.date

class Service(Base):
    __tablename__ = "main_service"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(String)

    def __str__(self):
        return f"{self.name} - {self.price} грн."


services = session.query(Service).all()
free_dates = session.query(FreeDate).filter(FreeDate.free==True)

