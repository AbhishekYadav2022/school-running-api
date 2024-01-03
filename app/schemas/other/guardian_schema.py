from datetime import datetime
from pydantic import BaseModel
from typing import Optional


# Schema For Creating Student
class CreateGuardian(BaseModel):
    first_name: str
    last_name: str
    phone: str

class GetGuardian(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str

    class Config:
        from_attributes = True