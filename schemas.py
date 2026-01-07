from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    role: str

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    capacity: int

class EventResponse(BaseModel):
    id: int
    title: str
    capacity: int

    class Config:
        from_attributes = True

class SubEventCreate(BaseModel):
    title: str
    start_time: str
    event_id: int

class SubEventResponse(BaseModel):
    id: int
    title: str
    start_time: str

    class Config:
        from_attributes = True