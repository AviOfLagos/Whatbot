from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Integer, String, PickleType
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()

Base = declarative_base()

class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    admin_name = Column(String(200), nullable=False)
    admin_phone = Column(String(20), nullable=False)
    members = Column(PickleType, nullable=False)
    total_members = Column(Integer, nullable=False)

class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False)
    text = Column(String(1000), nullable=False)
    timestamp = Column(DateTime, nullable=False)

def create_tables():
    Base.metadata.create_all(db.engine)
