from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


# Schema For Creating Student
class CreateStudent(BaseModel):
    first_name: str
    last_name: str
    father_name: str
    mother_name: str
    phone: str
    address: str
    guardian_id: int

class GetStudent(BaseModel):
    id: int
    last_name: str
    first_name: str
    father_name: str
    mother_name: str
    phone: str
    address: str
    guardian_id: int
    # todo: to add created_at table 

    class Config:
        from_attributes = True