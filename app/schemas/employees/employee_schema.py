from pydantic import BaseModel
from datetime import datetime


class CreateEmployee(BaseModel):
    first_name: str
    last_name: str
    phone: str
    address: str
    dept_id: int


class GetEmployee(BaseModel):
    emp_id: int
    first_name: str
    last_name: str
    phone: str
    address: str
    dept_id: int
    created_at: datetime

    class Config:
        from_attributes = True
