from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema For Creating Student
class CreateStudent(BaseModel):
    name: str
    father: str
    std_class: str
    phone: str

class GetStudent(BaseModel):
    id: int
    name: str
    father: str
    std_class: str
    phone: str
    created_at: datetime
    class Config:
        orm_mode = True
