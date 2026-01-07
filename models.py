from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="USER")

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    capacity = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id")) 
    
    sub_events = relationship("SubEvent", back_populates="parent_event")

class SubEvent(Base):
    __tablename__ = "sub_events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    start_time = Column(String)
    event_id = Column(Integer, ForeignKey("events.id"))
    parent_event = relationship("Event", back_populates="sub_events")

class Registration(Base):
    __tablename__ = "registrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    ticket_code = Column(String, unique=True)
    team_name = Column(String, nullable=True)
    team_size = Column(Integer, default=1)

class Announcement(Base):
    __tablename__ = "announcements"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    event_id = Column(Integer, ForeignKey("events.id"))