from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# Schema For Creating Student
class CreateSessionClass(BaseModel):
    session_id: int
    class_id: int

class GetSessionClass(BaseModel):
    session_id: int
    class_id: int

    class Config:
        from_attributes = True